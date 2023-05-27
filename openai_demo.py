#!/usr/bin/env python3
import os

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

chatHistory = [{"role": "user", "content": '''You are a role-playing dungeon game. At each step, describe what is happening in 1 to 3 sentences. Then give the player 4 options on how to proceed. One of the options should be logical, one cunning, one aggressive, and one completely ridiculous. Return the options as a list of strings. Start the game by describing who the player is and where they are, what they see.
Also describe what the user sees in a sentence, this is the image caption.
The output after each turn (including the starting turn) should be a JSON object with the keys: "description", "choices", "image caption".
This is a list of other characters they might encounter during the game:


[
  {"name": "Aelar Rivenhart", "bio": "A master archer and Elf princess who takes command of the wind and strikes every weakness of her enemies."},
  {"name": "Cynthia Brighthelm", "bio": "A quirky Human mage with a happy demeanor, turning her adversaries' spells against them."},
  {"name": "Argis the Bold", "bio": "King of the Dwarves, Argis fights with honor and commands his people with his indestructible hammer."},
  {"name": "Xirala Shadowdancer", "bio": "A sultry Tiefling rogue who can shift between the shadows, stealing without a trace."},
  {"name": "Baelgor Earthsplitter", "bio": "A wise Gnome druid with a deep connection to nature, wielding the earth itself as a weapon."},
  {"name": "Elara Nightstar", "bio": "A celestial Aasimar Cleric called to heal and protect the faithful, her radiance blinding enemies."},
  {"name": "Fizzlewick McFlambe", "bio": "An impulsive Halfling pyromancer who sets fire to the battlefield, leaving a trail of ashes in his wake."},
]
Respond only in JSON.
'''}]

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
print(text)
