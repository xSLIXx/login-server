
from flask import Flask, request, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump({}, f)
    with open(ACCOUNTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

@app.route("/")
def home():
    return "✅ Server läuft"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    key = data.get("key")
    hwid = data.get("hwid")

    accounts = load_accounts()

    if username not in accounts:
        return jsonify({"success": False, "message": "Benutzer nicht gefunden."})

    user = accounts[username]

    if user["password"] != password or user["key"] != key:
        return jsonify({"success": False, "message": "Falsche Zugangsdaten."})

    if user["expires_at"] != "lifetime":
        expires = datetime.strptime(user["expires_at"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expires:
            return jsonify({"success": False, "message": "Key abgelaufen."})

    if user.get("hwid") is None:
        user["hwid"] = hwid
        save_accounts(accounts)
    elif user["hwid"] != hwid:
        return jsonify({"success": False, "message": "Dieser Account ist an einen anderen PC gebunden."})

    return jsonify({"success": True})

@app.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()
    admin_user = data.get("admin")
    admin_pass = data.get("admin_pass")

    if admin_user != "SLIX" or admin_pass != "1a2b3d4C":
        return jsonify({"success": False, "message": "Keine Admin-Rechte."})

    new_user = data.get("username")
    new_pass = data.get("password")
    new_key = data.get("key")
    key_type = data.get("key_type")

    expires_at = "lifetime"
    if key_type == "24h":
        expires_at = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    elif key_type == "1w":
        expires_at = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d %H:%M:%S")
    elif key_type == "1m":
        expires_at = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    accounts = load_accounts()
    if new_user in accounts:
        return jsonify({"success": False, "message": "Benutzer existiert bereits."})

    accounts[new_user] = {
        "password": new_pass,
        "key": new_key,
        "expires_at": expires_at,
        "hwid": None
    }
    save_accounts(accounts)
    return jsonify({"success": True, "message": "Benutzer erstellt."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
