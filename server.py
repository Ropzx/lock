from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import random
import string

app = Flask(__name__)

tokens = {}
keys = {}

def generate_random_string(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>KGBB Unlock Portal</title>
</head>
<body style="background-color: black; color: lime; font-family: Courier New; text-align: center; padding-top: 100px;">
    <h1>KGBB Unlock Portal</h1>
    <form action="/verify" method="post">
        <input type="text" name="token" placeholder="Paste your token here" style="width: 300px; font-size: 18px;" required>
        <br><br>
        <input type="submit" value="Submit Token" style="font-size: 20px;">
    </form>

    {% if message %}
    <h2>{{ message }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_PAGE, message=None)

@app.route('/verify', methods=['POST'])
def verify():
    token = request.form.get('token')
    if token in tokens:
        unlock_key = tokens[token]
        message = f"✅ Your Unlock Key: {unlock_key}"
    else:
        message = "❌ Invalid token. Please try again."

    return render_template_string(HTML_PAGE, message=message)

@app.route('/register', methods=['POST'])
def register():
    token = generate_random_string(16)
    key = generate_random_string(8)
    tokens[token] = key
    return jsonify({"token": token})

@app.route('/unlock', methods=['POST'])
def unlock():
    data = request.get_json()
    token = data.get('token')
    if token in tokens:
        return jsonify({"key": tokens[token]})
    else:
        return jsonify({"error": "Invalid token."}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
