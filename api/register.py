from flask import Flask, request, jsonify
import json, os, uuid

app = Flask(__name__)

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        return json.load(open(USERS_FILE))
    return {}

def save_users(users):
    json.dump(users, open(USERS_FILE,"w"))

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    partner_code = data.get("partner_code")  # optional

    if not username or not password:
        return jsonify({"error":"Missing username or password"}),400

    users = load_users()
    if username in users:
        return jsonify({"error":"Username exists"}),400

    code = str(uuid.uuid4())[:6]
    users[username] = {"password":password,"partner":None,"code":code}

    if partner_code:
        for u, v in users.items():
            if v.get("code") == partner_code:
                users[username]["partner"]=u
                users[u]["partner"]=username
                break

    save_users(users)
    return jsonify({"message":"Registered","partner_code":users[username]["code"]})
