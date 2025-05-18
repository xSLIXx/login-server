from flask import Flask, request, jsonify

app = Flask(__name__)

# Beispielhafte Account-Daten (kann durch eine JSON-Datei ersetzt werden)
accounts = [
    {
        "username": "admin",
        "password": "1a2b3d4C.00",
        "key": "1a2b3d4C.00",
        "hwid": None  # wird beim ersten Login gesetzt

        "username": "Niro",
        "password": "1234",
        "key": "fa00378c-df42-4ea1-a8cf-92b4f2e9f3ba",
        "expiry": "2025-05-19",
        "hwid": ""

    }
]

@app.route("/", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Ungültige Anfrage"}), 400

    username = data.get("username")
    password = data.get("password")
    key = data.get("key")
    hwid = data.get("hwid")

    for acc in accounts:
        if acc["username"] == username and acc["password"] == password and acc["key"] == key:
            if acc["hwid"] is None:
                acc["hwid"] = hwid  # ersten HWID setzen
                return jsonify({"success": True, "message": "Login erfolgreich. HWID gespeichert."})
            elif acc["hwid"] == hwid:
                return jsonify({"success": True, "message": "Login erfolgreich."})
            else:
                return jsonify({"success": False, "message": "Falsche HWID."}), 403

    return jsonify({"success": False, "message": "Ungültige Zugangsdaten."}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
