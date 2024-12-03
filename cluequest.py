import wiki
import  ai
from data import categories


MAX_PLAYERS = 4
MIN_PLAYERS = 1
MAX_ROUNDS = 10
MIN_ROUNDS = 1
players_data = {}
AI = 'gpt'       # 'gemini' or 'gpt' possible



def display_welcome():
    print("=======================================")
    print("✨ \033[35mWelcome to ClueQuest! ✨\033[35m")
    print("=======================================")
    print("\033[30mAn exciting trivia game where you solve clues to guess the mystery Wikipedia article!")
    print("Compete against your opponent to see who can guess correctly with the fewest clues.")
    print("Get ready for thrilling fun!\033[30m")
    print("=======================================\n")


def display_description():
    print("\033[32mGame Rules:\033[32m")
    print("-----------")
    print("1. The game is played between 1-4 players over 3 rounds of guessing per game.")
    print("2. For every game, a random Wikipedia article is selected.")
    print("3. Each round, you will be given clues one at a time to guess the article.")
    print("4. Fewer clues = more points! But be careful, incorrect guesses can cost you.")
    print("5. The points look like this: \n     - First guess correct: 10 points."
          " \n     - Second guess correct: 5 points. \n"
          "     - 3rd guess correct: 3 points \n     - No correct guess: 0 points.")
    print("6. At the end of 3 rounds, the player with the highest score wins!")
    print("7. If you are playing multiple games, your score will be counted in the end.")
    print("\033[32m=======================================\n\033[32m")


def play_round(players_number, data, AI):
    show_categories(categories)
    for index in range(1, players_number + 1):  # Start from Player 1
        player_key = f"Player {index}"
        print(f"----------☘️ {player_key} IS PLAYING ☘️ -----------")
        if player_key in data:
            data[player_key] += wiki.play_game(ai.get_data(AI)) # Increment score (placeholder for actual logic)
        else:
            data[player_key] = wiki.play_game(ai.get_data(AI))   # Initialize player's score


def get_number(text='', min_num=1, max_num=4):
    """Prompt the user for a valid movie year within a defined range."""
    while True:
        print_text = text if text else "Enter a number: "
        value = input(print_text)
        if value.isdigit() and min_num <= int(value) <= max_num:
            return int(value)
        print("❌ Invalid input. Please enter a valid value ❌\n")


def get_winner(scores):
    # Find the highest score
    highest_score = max(scores.values())
    # Find all winners with the highest score
    winners = [name for name, score in scores.items() if score == highest_score]
    # Display the results
    if len(winners) > 1:
        return ', '.join(winners), highest_score
    else:
        return winners[0], highest_score


def show_result(scores):
    winner, highest_score = get_winner(scores)
    # Print the winner and their result
    print(f"\033[95mFINAL SCORE\033[95m:")
    for player, score in scores.items():
        print(f"{player}: {score} points ")
    print(f"🎉 {winner} is the ultimate winner! 🎉")
    print("Thank you for playing ✨ClueQuest✨\n "
          "⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐\n"
          "⭐⭐⭐⭐⭐⭐\033[95mGOODBYE\033[95m⭐⭐⭐⭐⭐⭐⭐\n"
          "⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐")


def inter_scoreboard(round_num, scores):
    winner, highest_score = get_winner(scores)
    print(f"-----Round {round_num} 🌀 Scoreboard:----- ")
    for player, score in scores.items():
        print(f"-------{player}: {score} points------- ")
    print(f"👏 {winner} is the winner of this round 👏")
    print("___Let's get onto the next round!___\n")


def show_categories(categories):
    print("Choose a category from the list\n")
    for value, category in categories.items():
        print(f"{value}. {category}")
    print('\n')


def main():
    display_welcome()
    display_description()
    players_number = get_number("\033[30mHow many players are you? : \033[30m", MIN_PLAYERS, MAX_PLAYERS )
    rounds_number = get_number("\033[30mHow many games do you want to play? 3 guesses per game : \033[30m", MIN_ROUNDS, MAX_ROUNDS)
    for round_num in range(1, rounds_number + 1):
        play_round(players_number, players_data, AI)
        inter_scoreboard(round_num, players_data)
    show_result(players_data)


if __name__ == "__main__":
    main()