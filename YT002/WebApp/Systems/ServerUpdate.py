import os
import json
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Retrieve the encryption key from an environment variable
key = os.getenv('FLASK_KEY')
if not key:
    raise Exception("Encryption key not set in environment variables.")
cipher = Fernet(key)

# Load user credentials from a local file
def load_users(filename='users.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_users(users, filename='users.json'):
    with open(filename, 'w') as f:
        json.dump(users, f)

users = load_users()

# Update user credentials securely
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    save_users(users)
    return jsonify({"message": "User registered successfully"}), 201

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Welcome to the Monster's Sanctuary!"

@app.route('/encrypt', methods=['POST'])
@auth.login_required
def encrypt():
    data = request.json.get('data', '')
    if not data:
        return jsonify({"error": "No data provided"}), 400
    encrypted_data = cipher.encrypt(data.encode())
    return jsonify({"encrypted_data": encrypted_data.decode()}), 200

@app.route('/decrypt', methods=['POST'])
@auth.login_required
def decrypt():
    encrypted_data = request.json.get('encrypted_data', '')
    if not encrypted_data:
        return jsonify({"error": "No data provided"}), 400
    try:
        decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
        return jsonify({"decrypted_data": decrypted_data}), 200
    except Exception as e:
        return jsonify({"error": "Decryption failed", "details": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
