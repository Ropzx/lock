from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Server memory
current_valid_token = None
unlock_key = None

@app.route('/', methods=['GET'])
def index():
    return 'KGBB API is running ✅'


def generate_unlock_key(length=8):
    """Generate random unlock key (A-Z, 0-9)"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/register', methods=['POST'])
def register_token():
    global current_valid_token, unlock_key

    data = request.json
    token = data.get('token')

    if token:
        # Save the new token
        current_valid_token = token
        unlock_key = generate_unlock_key()

        return jsonify({
            'status': 'registered',
            'message': 'Token registered successfully.'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'No token provided.'
        }), 400

@app.route('/unlock', methods=['POST'])
def unlock():
    data = request.json
    received_token = data.get('token')

    if received_token == current_valid_token:
        return jsonify({
            'status': 'success',
            'unlock_key': unlock_key
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid token'
        }), 403

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    entered_key = data.get('key')

    if entered_key == unlock_key:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error'}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
