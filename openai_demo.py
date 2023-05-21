#!/usr/bin/env python3
import requests

# load variables from .env file by evaluating the file as python code
OPENAI_API_KEY = None
DEEPAI_API_KEY = None
file = open('.env', 'r')
for line in file:
    if line[0] != '#':
        exec(line)

chatHistory = [{"role": "user", "content": "Write a Haiku about cats."}]

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
            "model": "gpt-4",
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
