from flask import Flask, render_template
from models import db, TriggerEvent
from api import api_bp
from auftrag import auftrag_bp
from event_status_update import status_bp
from time_utils import gruppiere_events_nach_auftrag
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://meineapiuser:gk2u1YcUpTDkqVlhZY0U0qAtGcBWxXcD@dpg-cvrvbcur433s73eaj0k0-a.oregon-postgres.render.com/meineapidb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(api_bp)
app.register_blueprint(auftrag_bp)
app.register_blueprint(status_bp)

@app.route("/")
def index():
    events = TriggerEvent.query.order_by(TriggerEvent.execute_at).all()
    auftraege = gruppiere_events_nach_auftrag(events)
    return render_template("status.html", auftraege=auftraege)

@app.route("/admin")
def admin():
    events = TriggerEvent.query.order_by(TriggerEvent.execute_at).all()
    auftraege = gruppiere_events_nach_auftrag(events)
    return render_template("admin.html", auftraege=auftraege)

@app.route("/auftrag/<int:auftrag_id>")
def auftrag_detail(auftrag_id):
    events = TriggerEvent.query.filter_by(auftrag_id=auftrag_id).order_by(TriggerEvent.execute_at).all()

    # Lade Testsets aus JSON
    with open("testsets.json", "r") as f:
        testsets_data = json.load(f)

    # Extrahiere gewählte Testsets aus Events (z. B. run-test)
    testset_namen = []
    for e in events:
        if e.type == "run-test" and e.testsets:
            testset_namen = e.testsets
            break

    # Baue Detail-Daten für Anzeige
    details = []
    for testset_name in testset_namen:
        cases = testsets_data.get(testset_name, [])
        details.append({
            "name": testset_name,
            "testcases": cases
        })

    return render_template("detail.html", auftrag_id=auftrag_id, events=events, details=details)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
