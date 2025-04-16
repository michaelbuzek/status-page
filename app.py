from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

from models import db
from api import api_bp
from auftrag import auftrag_bp
from event_status_update import status_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meineapiuser:gk2u1YcUpTDkqVlhZY0U0qAtGcBWxXcD@dpg-cvrvbcur433s73eaj0k0-a.oregon-postgres.render.com/meineapidb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

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
    from models import TriggerEvent
    items = TriggerEvent.query.order_by(TriggerEvent.execute_at.asc()).all()
    return render_template("status.html", items=items)

@app.route("/admin")
def admin():
    from models import TriggerEvent
    items = TriggerEvent.query.order_by(TriggerEvent.execute_at.asc()).all()
    return render_template("admin.html", items=items)


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
def api_add_order():
    req_data = request.get_json()
    required_fields = ["order_id", "date", "router", "fw", "runs"]
    if not all(field in req_data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    data = load_data()
    new_order = {
        "order_id": req_data["order_id"],
        "date": req_data["date"],
        "router": req_data["router"],
        "fw": req_data["fw"],
        "status": "PENDING",
        "runs": req_data["runs"],
        "report": req_data.get("report", "")
    }
    data.append(new_order)
    save_data(data)
    return jsonify({"message": "Order added"}), 201

@app.route("/api/delete", methods=["DELETE"])
def api_delete_order():
    req_data = request.get_json()
    order_id = str(req_data.get("order_id"))
    data = load_data()
    new_data = [item for item in data if str(item.get("order_id")) != order_id]
    if len(new_data) == len(data):
        return jsonify({"error": "Item not found"}), 404
    save_data(new_data)
    return jsonify({"message": "Order deleted"}), 200

@app.route("/delete/<order_id>", methods=["GET"])
def delete_order_admin(order_id):
    data = load_data()
    data = [item for item in data if str(item["order_id"]) != str(order_id)]
    save_data(data)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
