from flask import Flask, request, jsonify
import uuid
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DATA_FILE = 'data.json'

# Lade bestehende Daten oder initialisiere eine leere Liste
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        users = json.load(f)
else:
    users = []

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    key = data.get('key')
    hwid = data.get('hwid')

    for user in users:
        if user['username'] == username and user['password'] == password and user['key'] == key:
            expiry_date = datetime.strptime(user['expiry'], '%Y-%m-%d')
            if datetime.now() > expiry_date:
                return jsonify({'success': False, 'message': 'Key abgelaufen'})
            if user['hwid'] == '' or user['hwid'] == hwid:
                user['hwid'] = hwid
                save_data()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'HWID nicht gültig'})
    return jsonify({'success': False, 'message': 'Ungültige Anmeldedaten'})

@app.route('/admin', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'Admin' and password == '1a2b3d4C.00':
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Ungültige Admin-Anmeldedaten'})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    validity_days = data.get('validity_days')

    new_user = {
        'username': username,
        'password': password,
        'key': str(uuid.uuid4()),
        'expiry': (datetime.now() + timedelta(days=validity_days)).strftime('%Y-%m-%d'),
        'hwid': ''
    }
    users.append(new_user)
    save_data()
    return jsonify({'success': True, 'user': new_user})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
