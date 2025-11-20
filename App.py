from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# Funktion zum Auslesen der aktuellen Position
def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Funktion zum Speichern einer neuen Position
def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Startseite: zeigt aktuelle Position
@app.route("/")
def index():
    data = read_data()
    return render_template("index.html", position=data["position"])

# Endpoint zum Aktualisieren der Position
@app.route("/update", methods=["POST"])
def update():
    new_pos = request.json.get("position")
    if new_pos:
        write_data({"position": new_pos})
        return jsonify({"status": "ok", "position": new_pos})
    return jsonify({"status": "error"}), 400

# Endpoint zum Abrufen der aktuellen Position (für Live-Updates)
@app.route("/data", methods=["GET"])
def data():
    return jsonify(read_data())

# App starten, Port dynamisch setzen für Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
