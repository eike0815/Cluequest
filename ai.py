import os
from dotenv import load_dotenv
from data import categories, topics
import openai
import google.generativeai as genai
import re


MAX_WORD_LENGTH = 30


# load keys
load_dotenv(".env")
GPT_KEY = os.getenv("GPT_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Chat GPT
openai.api_key = GPT_KEY
# Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def choosing_category_from_list(categories):
    chosen_category = input("Enter category (number or entire name): ")
    print("\n")
    print(".......🗼..⭐...Fetching data...⭐..🗼........")
    print("🌍..🚴‍...Please wait (up to 1 minute)...🚴‍♂️..🌍")
    print("\n")
    return categories[chosen_category]


def remove_symbols(input_string):
    # Keep only letters (both uppercase and lowercase)
    return re.sub(r'[^a-zA-Z\s]', '', input_string)


def remove_words_in_parentheses(text):
    # Remove text within parentheses and the parentheses themselves
    return re.sub(r'\(.*?\)', '', text).strip()


def create_list(data, titel):
    new_list = []
    items = data.split('\n')
    for line in items:
        if line.strip() and len(line) < MAX_WORD_LENGTH:  # Ignore empty lines and prevent big names
            # Remove the number and dash or dot at the start, if present
            if line[0].isdigit() or line[0] == "*":
                # If it starts with a number and a separator, remove it
                line = line.split(' ', 1)[-1].strip()
            new_list.append(remove_words_in_parentheses(line).strip())
    new_list.insert(0, remove_symbols(titel))
    # print(new_list)
    return new_list

def get_data(ai):
    topic = choosing_category_from_list(categories)
    data = topics[topic]
    if ai == 'gpt':
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "user", "content": data}])
        return create_list(response['choices'][0]['message']['content'], topic)
    elif ai == 'gemini':
        response = model.generate_content(data)
        return create_list(response.text, topic)