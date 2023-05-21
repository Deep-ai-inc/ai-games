#!/usr/bin/env python3
# Flask Server:
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# load variables from .env file by evaluating the file as python code
OPENAI_API_KEY = None
DEEPAI_API_KEY = None
file = open('.env', 'r')
for line in file:
    if line[0] != '#':
        exec(line)

print(OPENAI_API_KEY)
print(DEEPAI_API_KEY)

# define app:
app = Flask(__name__, template_folder='./templates')


# route to the main page
@app.route('/')
def main():
    return render_template('index.html')


# route that takes in JSON (post) and returns JSON:

@app.route('/text_api', methods=['POST'])
def text_api():
    # get the JSON data from the request
    data = request.get_json()
    print("data: ", data)
    # get the text from the JSON
    chatHistory = data['chatHistory']
    # make the request to the OpenAI API
    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=text,
    #     temperature=0.9,
    #     max_tokens=100,
    #     top_p=1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0,
    #     stop=["\n", " Human:", " AI:"]
    # )

    # chatHistory = [{"role": "user", "content": text}]

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

    # return the response as JSON
    return jsonify({'text': text})


# now make image API that uses DeepAI Text to Image API

@app.post('/image_api')
def image_api():
    # get the JSON data from the request
    data = request.get_json()

    # make the request to the DeepAI API
    resp = requests.post(
        "https://api.deepai.org/api/text2img",
        headers={
            "api-key": DEEPAI_API_KEY,
        },
        data=data
    )
    print("sent request to deepai")
    print(resp.content)
    resp.raise_for_status()
    response = resp.json()
    print("response from deepai: ", response)

    # get actual image url from response:
    image_url = response['output_url']

    # return the response as JSON
    return jsonify({'image_url': image_url})

# upscale image using deepai torch-srgan api
@app.post('/upscale_api')
def upscale_api():
    # get the JSON data from the request
    data = request.get_json()

    # make the request to the DeepAI API
    resp = requests.post(
        "https://api.deepai.org/api/torch-srgan",
        headers={
            "api-key": DEEPAI_API_KEY,
        },
        data=data
    )
    print("sent request to deepai")
    print(resp.content)
    resp.raise_for_status()
    response = resp.json()
    print("response from deepai: ", response)

    # get actual image url from response:
    image_url = response['output_url']

    # return the response as JSON
    return jsonify({'image_url': image_url})

# Call like this:
# curl -X POST -d '{"text":"write haiku"}' -H 'Content-Type: application/json' http://127.0.0.1:5432/text_api

# run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5432)

