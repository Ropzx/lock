from flask import Flask, request, jsonify, render_template
import random
import string

app = Flask(__name__)

# Temporary storage of tokens and keys
VALID_TOKENS = {}

def generate_random_key(length=8):
    """Generate random unlock key"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/', methods=['GET'])
def homepage():
    """Landing page"""
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate_token():
    """Handle token submission"""
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400

    if token in VALID_TOKENS:
        unlock_key = VALID_TOKENS[token]
    else:
        unlock_key = generate_random_key()
        VALID_TOKENS[token] = unlock_key

    return jsonify({"unlock_key": unlock_key})

@app.route('/admin/list', methods=['GET'])
def list_tokens():
    """Optional admin view of all tokens (secure this in production!)"""
    return jsonify(VALID_TOKENS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
