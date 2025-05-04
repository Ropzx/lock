from flask import Flask, request, jsonify, render_template
import random
import string
import os

app = Flask(__name__)

tokens = {}  # token -> unlock_key

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route('/')
def home():
    return render_template('index.html')  # Serve frontend

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token missing"}), 400

    unlock_key = generate_key()
    tokens[token] = unlock_key

    print(f"Token {token} registered with unlock_key {unlock_key}")  # Debug output

    return jsonify({"message": "Token registered successfully."}), 200

@app.route('/get_key', methods=['POST'])
def get_key():
    data = request.get_json()
    token = data.get("token")
    print(f"Received request for /get_key with token: {token}")  # Debug output

    if not token or token not in tokens:
        print(f"Token {token} not found.")  # Debug output
        return jsonify({"error": "Invalid token."}), 400

    unlock_key = tokens[token]
    print(f"Returning unlock_key {unlock_key} for token {token}")  # Debug output

    return jsonify({"unlock_key": unlock_key}), 200

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    key = data.get("key")
    if not key:
        return jsonify({"error": "Key missing."}), 400

    if key in tokens.values():
        # Remove the token associated with this key
        token_to_delete = None
        for token, stored_key in tokens.items():
            if stored_key == key:
                token_to_delete = token
                break

        if token_to_delete:
            del tokens[token_to_delete]

        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failure"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
