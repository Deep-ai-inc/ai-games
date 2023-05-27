#!/usr/bin/env python3
import os
from os import system

import requests

# load variables from .env file by evaluating the file as python code
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


def generate_game_images():
    for game in games:
        for i in range(3):
            resp = requests.post(
                "https://api.deepai.org/api/text2img",
                headers={
                    "api-key": DEEPAI_API_KEY,
                },
                data={
                    'text': game,
                    "negative_prompt":"nude nudity, cropped, deformed, drawing, cartoon, grid, text, caption, playing card, trading card",
                    'grid_size': 1,
                }
            )
            print("sent request to deepai")
            print(resp.content)
            try:
                resp.raise_for_status()
            except:
                print("error: ", resp.content)
                continue
        response = resp.json()
        print("response from deepai: ", response)

        # get actual image url from response:
        image_url = response['output_url']

        # save the image to a file
        resp = requests.get(image_url)
        resp.raise_for_status()
        os.makedirs('images/games', exist_ok=True)
        with open('images/games/' + game + '.jpg', 'wb') as f:
            f.write(resp.content)


generate_game_images()
