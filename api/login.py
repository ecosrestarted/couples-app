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

@app.route("/", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    if username not in users:
        return jsonify({"error":"User not found"}), 404

    hashed = hashlib.sha256(password.encode()).hexdigest()
    if hashed != users[username]["password"]:
        return jsonify({"error":"Incorrect password"}), 401

    return jsonify({"message":"Login successful"})

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
