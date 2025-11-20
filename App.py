from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/")
def index():
    data = read_data()
    return render_template("index.html", position=data["position"])

@app.route("/update", methods=["POST"])
def update():
    new_pos = request.json.get("position")
    if new_pos:
        write_data({"position": new_pos})
        return jsonify({"status": "ok", "position": new_pos})
    return jsonify({"status": "error"}), 400

@app.route("/data", methods=["GET"])
def data():
    return jsonify(read_data())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
