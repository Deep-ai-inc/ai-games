#!/usr/bin/env python3
# Flask Server:
import json
import os
import sys

import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
import sseclient

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

# define app:
app = Flask(__name__, template_folder='./templates')

# serve images from the /images directory
app.static_folder = 'images'

# route to the main page
@app.route('/')
def main():
    return render_template('index.html')


# route for the game page:
@app.route('/game')
def game():
    return render_template('game.html')


# route for text to image page:
@app.route('/text_to_image')
def text_to_image():
    return render_template('text_to_image.html')


# route for text generation page:
@app.route('/text_generation')
def text_generation():
    return render_template('text_generation.html')



# route that takes in JSON (post) and returns JSON:

def generate_response(requests_resp):
    # return resp.content
    total_response = ''
    client = sseclient.SSEClient(requests_resp)
    for event in client.events():
        if event.data == "[DONE]":
            print("\n\ndone")
            break

        try:
            parsed = json.loads(event.data)
            # print("parsed: ", parsed)
        except Exception as e:
            print("error parsing json: ", e)
            print("event.data: ", event.data)
            continue

        # we want to return the "content" field
        if 'choices' in parsed:
            # print(parsed['choices'][0]['delta']['content'])
            if 'content' in parsed['choices'][0]['delta']:

                text = parsed['choices'][0]['delta']['content']
                total_response += text
                sys.stdout.write(text)
                sys.stdout.flush()
            else:
                # print("no content field in this chunk: ", parsed)
                pass

    return total_response


@app.route('/text_api', methods=['POST'])
def text_api():
    # get the JSON data from the request
    data = request.get_json()
    print("data: ", data)
    # get the text from the JSON
    chatHistory = data['chatHistory']

    stream = True
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
            "stream": True
        },
        stream=True
    )
    print("sent request to openai\n\n")
    if stream:

        # return resp.content as a streaming response

        return generate_response(resp), {"Content-Type": "text/plain"}
        # return jsonify({'text': total_response})

    else:
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
# curl -X POST -d '{"chatHistory":[{"role": "user", "content":"write haiku about dogs"}]}' -H 'Content-Type: application/json' http://127.0.0.1:5432/text_api
# run the app
# if __name__ == '__main__':

# The reloader broke under replit, so I'm disabling it

app.run(debug=True, host='0.0.0.0', use_reloader=False, port=5432)
print("!!server running")
