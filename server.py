from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

tokens = {}  # token -> unlock_key

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token missing"}), 400

    # Generate unlock key for this token
    unlock_key = generate_key()
    tokens[token] = unlock_key

    return jsonify({"message": "Token registered successfully."}), 200

@app.route("/get_key", methods=["POST"])
def get_key():
    data = request.get_json()
    token = data.get("token")
    if not token or token not in tokens:
        return jsonify({"error": "Invalid token."}), 400

    return jsonify({"unlock_key": tokens[token]}), 200

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    key = data.get("key")
    if not key:
        return jsonify({"error": "Key missing."}), 400

    # Check if key matches any registered unlock key
    if key in tokens.values():
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failure"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
