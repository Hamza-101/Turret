# #INSTALL FIREWALL
# Add encryption etc.


# import os
# from flask import Flask, request, jsonify
# from flask_httpauth import HTTPBasicAuth
# from cryptography.fernet import Fernet
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Retrieve the encryption key from an environment variable
# key = os.getenv('FLASK_KEY')
# if not key:
#     raise Exception("Encryption key not set in environment variables.")
# cipher = Fernet(key)

# # Store user credentials securely (hashed passwords)
# users = {
#     "Monster": generate_password_hash("17_AreYouAlive_23")  # Example of a strong hashed password
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users[username], password):
#         return username

# @app.route('/')
# @auth.login_required
# def index():
#     return "Welcome to the Monster's Sanctuary!"

# @app.route('/encrypt', methods=['POST'])
# @auth.login_required
# def encrypt():
#     data = request.json.get('data', '')
#     if not data:
#         return jsonify({"error": "No data provided"}), 400
#     encrypted_data = cipher.encrypt(data.encode())
#     return jsonify({"encrypted_data": encrypted_data.decode()}), 200

# @app.route('/decrypt', methods=['POST'])
# @auth.login_required
# def decrypt():
#     encrypted_data = request.json.get('encrypted_data', '')
#     if not encrypted_data:
#         return jsonify({"error": "No data provided"}), 400
#     try:
#         decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
#         return jsonify({"decrypted_data": decrypted_data}), 200
#     except Exception as e:
#         return jsonify({"error": "Decryption failed", "details": str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=False)

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Define a username and password (for demonstration only; use hashed passwords in production)
USERNAME = 'admin'
PASSWORD = 'password123'

# Function to check credentials
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# Function to prompt for authentication
def authenticate():
    return Response(
        'Could not verify your login!\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Check if credentials are valid
@app.before_request
def before_request():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@app.route('/')
def index():
    return "Welcome to the Password Protected Server!"

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({"data": "This is some secure data!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
