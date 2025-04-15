# version 19-30 final clean
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

from models import db
from api import api_bp
from auftrag import auftrag_bp
from event_status_update import status_bp

app = Flask(__name__)

# PostgreSQL für Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meineapiuser:gk2u1YcUpTDkqVlhZY0U0qAtGcBWxXcD@dpg-cvrvbcur433s73eaj0k0-a.oregon-postgres.render.com/meineapidb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Blueprints
app.register_blueprint(api_bp)
app.register_blueprint(auftrag_bp)
app.register_blueprint(status_bp)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    data = load_data()
    return render_template("status.html", items=data)

@app.route("/admin", methods=["GET"])
def admin():
    data = load_data()
    return render_template("admin.html", items=data)

@app.route("/add", methods=["POST"])
def add_order():
    data = load_data()
    new_order = {
        "order_id": request.form["order_id"],
        "date": request.form["date"],
        "router": request.form["router"],
        "fw": request.form["fw"],
        "status": "PENDING",
        "runs": request.form.getlist("runs"),
        "report": ""
    }
    data.append(new_order)
    save_data(data)
    return redirect(url_for("admin"))

@app.route("/delete", methods=["POST"])
def delete_order():
    order_id = request.form.get("order_id")
    data = load_data()
    data = [item for item in data if str(item.get("order_id")) != str(order_id)]
    save_data(data)
    return redirect(url_for("admin"))

@app.route("/update", methods=["POST"])
def update_order():
    req_data = request.get_json()
    order_id = str(req_data.get("order_id"))
    data = load_data()
    found = False
    for item in data:
        if str(item.get("order_id")) == order_id:
            if "status" in req_data:
                item["status"] = req_data["status"]
            if "report" in req_data:
                item["report"] = req_data["report"]
            found = True
            break
    if found:
        save_data(data)
        return jsonify({"message": "Order updated"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route("/api/orders", methods=["GET"])
def api_get_orders():
    data = load_data()
    return jsonify(data), 200

@app.route("/api/add", methods=["POST"])
def api_add_
