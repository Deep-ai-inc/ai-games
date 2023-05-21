#!/usr/bin/env python3
# Flask Server:

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# load variables from .env file by evaluating the file as python code
OPENAI_API_KEY = None
file = open('.env', 'r')
for line in file:
    if line[0] != '#':
        exec(line)

print(OPENAI_API_KEY)

# define app:
app = Flask(__name__, template_folder='./templates')


# route to the main page
@app.route('/')
def main():
    return render_template('index.html')

# run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5432)

