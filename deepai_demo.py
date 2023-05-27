#!/usr/bin/env python3
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


# call DeepAI Text To Image API

resp = requests.post(
    "https://api.deepai.org/api/text2img",
    headers={
        "api-key": DEEPAI_API_KEY,
    },
    data={
        'text': 'A happy dog',
        'grid_size': 1,
    }
)
print("sent request to deepai")
print(resp.content)
resp.raise_for_status()
response = resp.json()
print("response from deepai: ", response)

# get actual image url from response:
image_url = response['output_url']

# call DeepAI Torch SRGAN API

resp = requests.post(
    "https://api.deepai.org/api/torch-srgan",
    headers={
        "api-key": DEEPAI_API_KEY,
    },
    data={
        'image': image_url,
    }
)
print("sent request to deepai")
print(resp.content)
resp.raise_for_status()
response = resp.json()
print("response from deepai: ", response)

# get actual image url from response:
image_url = response['output_url']

# open the image in the browser
system('open ' + image_url)
