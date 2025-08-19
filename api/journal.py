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
def add_entry():
    data = request.json
    username = data.get("username")
    entry = data.get("entry")

    users = load_users()
    if username not in users:
        return jsonify({"error":"User not found"}), 404

    users[username]["journal"].append(entry)
    save_users(users)
    return jsonify({"message":"Entry added"})

@app.route("/", methods=["GET"])
def get_journal():
    username = request.args.get("username")
    users = load_users()
    if username not in users:
        return jsonify({"error":"User not found"}), 404
    return jsonify({"journal": users[username]["journal"]})

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
