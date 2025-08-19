from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, hashlib

app = Flask(__name__)
CORS(app)

DATA_FILE = "users.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

@app.route("/", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    users = load_users()
    if username in users:
        return jsonify({"error": "Username exists"}), 400

    hashed = hashlib.sha256(password.encode()).hexdigest()
    users[username] = {"password": hashed, "journal": []}
    save_users(users)
    return jsonify({"message": "Registered successfully"})

# serverless handler for Vercel
def handler(environ, start_response):
    from werkzeug.wrappers import Request
    request_ = Request(environ)
    with app.test_request_context(
        path=request_.path,
        method=request_.method,
        headers=request_.headers,
        data=request_.get_data()
    ):
        response = app.full_dispatch_request()
        return response(environ, start_response)
