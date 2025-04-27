from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

tokens = {}
keys = {}

def generate_random_string(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET'])
def index():
    return 'KGBB API is running ✅'

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
