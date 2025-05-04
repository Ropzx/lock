**# === server.py ===**
from flask import Flask, request, jsonify, render_template
import random
import string

app = Flask(__name__)

tokens = {}  # token -> unlock_key

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route('/')
def home():
    return "Server is running."

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token missing"}), 400

    unlock_key = generate_key()
    tokens[token] = unlock_key
    return jsonify({"message": "Token registered successfully."}), 200

@app.route('/get_key', methods=['POST'])
def get_key():
    data = request.get_json()
    token = data.get("token")
    if not token or token not in tokens:
        return jsonify({"error": "Invalid token."}), 400

    return jsonify({"unlock_key": tokens[token]}), 200

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    key = data.get("key")
    if not key:
        return jsonify({"error": "Key missing."}), 400

    if key in tokens.values():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


**# === client.py ===**
import requests
import random
import string

url = "https://kgbb.xyz"  # Update if running locally or on another host

def generate_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

token = generate_token()
print(f"Generated token: {token}")

try:
    register_response = requests.post(f"{url}/register", json={"token": token}, timeout=10)
    print("Register response:", register_response.json())

    input("Go to kgbb.xyz and enter the token above. Press Enter once you get the unlock key...")

    get_key_response = requests.post(f"{url}/get_key", json={"token": token}, timeout=10)
    print("Raw get_key response:", get_key_response.text)
    unlock_key = get_key_response.json().get("unlock_key")

    print(f"Received unlock key: {unlock_key}")
    user_input = input("Enter unlock key: ")

    if user_input == unlock_key:
        verify_response = requests.post(f"{url}/verify", json={"key": unlock_key}, timeout=10)
        if verify_response.ok and verify_response.json().get("status") == "success":
            print("✅ Unlock successful!")
        else:
            print("❌ Verification failed.")
    else:
        print("❌ Incorrect key entered.")

except Exception as e:
    print("Request failed:", e)
