import wikipedia
import random
import re
from difflib import SequenceMatcher


def get_random_movie(items_in_list):
    first_element = items_in_list[0]  # First element always in parentheses
    rest_of_elements = items_in_list[1:]  # Rest of the elements for random selection

    for _ in range(5):  # Retry up to 5 times
        try:
            title = random.choice(rest_of_elements)  # Select a random title from the rest
            # Format the title by appending the first element in parentheses
            formatted_title = f"{title} ({first_element})"
            content = wikipedia.summary(formatted_title, sentences=7)  # Fetch first 7 sentences
            return formatted_title, title, content  # Return formatted title, unformatted title, and content
        except wikipedia.exceptions.WikipediaException:
            continue
    return None, None, None  # Return None if all retries fail


def replace_similar_words(input_word, text, threshold=0.8):
    words = text.split()  # Split the text into words
    replaced_words = []

    for word in words:
        similarity = SequenceMatcher(None, input_word, word).ratio()
        if similarity >= threshold:  # Replace similar words with underscores
            replaced_words.append("____")
        else:
            replaced_words.append(word)

    return ' '.join(replaced_words)


def mask_name(title, content):
    list_of_words_in_title = title.split()
    masked_content = content  # Initialize the content with the original
    for word in list_of_words_in_title:
        # Mask the name in the content.
        masked_content = re.sub(rf'\b{re.escape(word)}\b', "_____", masked_content, flags=re.IGNORECASE)
    return masked_content


def split_content(masked_content):
    sentences = masked_content.split('. ')  # Split content into sentences
    valid_facts = []

    for sentence in sentences[1:]:
        if len(sentence) >= 20:  # Ensure fact length is at least 20 characters
            valid_facts.append(sentence)

    return valid_facts[:3]  # Return only the first 3 valid facts


def is_partial_match(title, guess):
    """
    Check if the user's guess matches any significant part of the title.
     Normalize the title and guess to lowercase and remove insignificant words
    """
    insignificant_words = {"the", "of", "a", "an", "in", "on", "at", "to", "and", "for", "with"}
    title_phrases = [phrase.lower() for phrase in re.split(r'[,:]', title) if phrase.strip()]
    title_significant_words = set(word.lower() for word in title.split() if word.lower() not in insignificant_words)
    guess_words = set(word.lower() for word in guess.split())

    # Check if the guess matches any significant phrase or contains all significant words
    if any(phrase in guess.lower() for phrase in title_phrases):
        return True
    return title_significant_words.issubset(guess_words)


def play_game(list_generated):
    print("🐋..🇩🇪...Hints are being generated (please wait)...🇩🇪..🐋")
    print("\n")
    formatted_title, title, content = get_random_movie(list_generated)  # Now get all three values
    if not formatted_title or not title or not content:
        print("Failed to fetch details. Please try again later!\n")
        return
    masked_content = replace_similar_words(formatted_title,mask_name(formatted_title, content))
    facts = split_content(masked_content)  # Ensure facts are long enough

    if len(facts) < 3:
        print("Not enough valid facts available. Please try again later!\n")
        return

    print("Here are your hints:")
    total_score = 0  # Initialize the score

    for idx, fact in enumerate(facts, start=1):
        print(f"Hint {idx}: {fact}\n")
        guess = input(f"Your guess (Hint {idx}): ").strip()

        # Check if the guess matches the unformatted title
        if is_partial_match(title, guess):
            points = 10 if idx == 1 else 5 if idx == 2 else 3
            total_score += points
            print(f"💪 Correct! It's '{title}'. You earned {points} points. 💪\n")
            break
        else:
            print("❌ Incorrect guess! ❌\n")

    print(f"The correct answer was: {title}.")
    print(f"Your score for this round: {total_score} points.\n")
    return total_score