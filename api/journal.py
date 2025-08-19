from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
JOURNAL_FILE = "journal.json"
USERS_FILE = "users.json"

def load_journal():
    if os.path.exists(JOURNAL_FILE):
        return json.load(open(JOURNAL_FILE))
    return {}

def save_journal(journal):
    json.dump(journal, open(JOURNAL_FILE,"w"))

def load_users():
    if os.path.exists(USERS_FILE):
        return json.load(open(USERS_FILE))
    return {}

@app.route("/api/journal", methods=["POST"])
def add_entry():
    data = request.json
    username = data.get("username")
    entry = data.get("entry")
    if not username or not entry:
        return jsonify({"error":"Missing username or entry"}),400

    journal = load_journal()
    users = load_users()
    partner = users.get(username,{}).get("partner")

    if username not in journal: journal[username]=[]
    journal[username].append(entry)

    # Add entry to shared journal if partner exists
    if partner:
        if partner not in journal: journal[partner]=[]
        journal[partner].append(f"{username}: {entry}")

    save_journal(journal)
    return jsonify({"message":"Entry added"})

@app.route("/api/journal", methods=["GET"])
def get_entries():
    username = request.args.get("username")
    if not username: return jsonify({"error":"Missing username"}),400
    journal = load_journal()
    return jsonify({"journal":journal.get(username,[])})
