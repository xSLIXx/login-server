from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Beispielhafte Account-Daten mit Ablaufdatum (YYYY-MM-DD)
accounts = [
    {
        "username": "admin",
        "password": "1a2b3d4C.00",
        "key": "1a2b3d4C.00",
        "hwid": None,
        "expires_at": "2099-12-31"  
    },
    {
        "username": "Niro",
        "password": "1234",
        "key": "dae72ede-a0cc-4c82-8893-8f80ee514a1b",
        "hwid": None,
        "expires_at": "2099-05-18"  
    },
    {
       "username": "Chapo",
        "password": "343!.0",
        "key": "9179e323-f472-4ae7-a507-97d1e0eec1a4",
        "hwid": None,
        "expires_at": "20925-05-26"
    },
    {
        "username": "Tariq",
        "password": "3436",
        "key": "d90a8ba5-a552-455f-b8b7-b1d9c65ee936",
        "hwid": None,
        "expires_at": "20929-05-26"
    },
    {
        "username": "Brunox",
        "password": "3436",
        "key": "dca39d35-30dc-4ecc-a297-166e44db477c",
        "hwid": None,
        "expires_at": "20929-05-26"
    },
    {
        "username": "Hans",
        "password": "3436",
        "key": "36d4ae50-08d4-46f1-8951-03ace28cceed",
        "hwid": None,
        "expires_at": "20929-05-26"
    },

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

            # Ablaufdatum prüfen
            expires_at = datetime.strptime(acc["expires_at"], "%Y-%m-%d")
            if datetime.now() > expires_at:
                return jsonify({"success": False, "message": "Key abgelaufen."}), 403

            if acc["hwid"] is None:
                acc["hwid"] = hwid
                return jsonify({"success": True, "message": "Login erfolgreich. HWID gespeichert."})
            elif acc["hwid"] == hwid:
                return jsonify({"success": True, "message": "Login erfolgreich."})
            else:
                return jsonify({"success": False, "message": "Falsche HWID."}), 403

    return jsonify({"success": False, "message": "Ungültige Zugangsdaten."}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
