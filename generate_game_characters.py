#!/usr/bin/env python3
import json
import os
from os import system

import requests

# load variables from .env or environment variables file by evaluating the file as python code
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
DEEPAI_API_KEY = os.environ.get('DEEPAI_API_KEY')
if os.path.exists('.env'):
    file = open('.env', 'r')
    for line in file:
        if line[0] != '#':
            exec(line)

print(OPENAI_API_KEY)
print(DEEPAI_API_KEY)


# generate image using deepai text2img api

games = [
    "Inception",
    "The Lord of the Rings Trilogy",
    "The Matrix Series",
    "Harry Potter Series",
    "The Godfather",
    "Pirates of the Caribbean",
    "Star Wars Franchise",
    "Jurassic Park",
    "The Chronicles of Narnia",
    "The Hunger Games Series",
    "The Silence of the Lambs",
    "Indiana Jones Series",
    "The Wizard of Oz",
    "Alice in Wonderland",
    "The Avengers Series",
    "Blade Runner",
    "The Dark Tower Series",
    "Ender's Game"
]

os.makedirs('game_characters_json', exist_ok=True)


def generate_game_characters():
    for game in games:
        output_filename = 'game_characters_json/{}.json'.format(game)

        # if file already exists, skip
        if os.path.exists(output_filename):
            print("skipping {} because it already exists".format(output_filename))
            continue

        prompt = '''write 1-sentence bio's of 5 random characters in a role-playing game taking place in "{}".
    the characters should have a name.
    respond as a JSON array with keys "name", "bio". Respond only in JSON.'''.format(game)

        chatHistory = [{"role": "user", "content": prompt}]

        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + OPENAI_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "max_tokens": 256,
                "top_p": 1,
                "presence_penalty": 0,
                "frequency_penalty": 0,

                "temperature": 1.0,
                "model": "gpt-3.5-turbo",
                "messages": chatHistory,
            }
        )
        print("sent request to openai")
        print(resp.content)
        resp.raise_for_status()
        response = resp.json()
        print("response from openai: ", response)

        # get actual text from response:
        text = response['choices'][0]['message']['content']
        #print(text)

        # check that it is valid json
        try:
            json.loads(text)
        except:
            print("error: response is not valid json")
            continue


        # write to file
        with open(output_filename, 'w') as f:
            f.write(text)



generate_game_characters()


# now read all the saved json files and combine them into one big json file

all_games = {}
for game in games:

    with open('game_characters_json/{}.json'.format(game), 'r') as f:
        characters = json.load(f)
        all_games[game] = characters

with open('game_characters_combined.json', 'w') as f:
    json.dump(all_games, f, indent=4)

print("wrote combined json file to game_characters_combined.json")
