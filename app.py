from flask import Flask, render_template
from models import db, TriggerEvent
from api import api_bp
from auftrag import auftrag_bp
from event_status_update import status_bp
from time_utils import gruppiere_events_nach_auftrag
from sqlalchemy import text
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

    # Lade Testset-Definitionen
    with open("testsets.json", "r") as f:
        testsets_data = json.load(f)

    # Ermitteltes Testsets aus dem run-test Event
    testset_namen = []
    for e in events:
        if e.type == "run-test" and e.testsets:
            testset_namen = e.testsets
            break

    # Lade result_map aus Datenbank (case_id → status)
    result_query = text("SELECT case_id, status FROM test_results WHERE auftrag_id = :aid")
    with db.engine.connect() as conn:
        result_data = conn.execute(result_query, {"aid": auftrag_id}).fetchall()
        result_map = {row[0]: row[1] for row in result_data}

    # Erstelle detail-Objekt für die Anzeige
    details = []
    for testset_name in testset_namen:
        set_info = testsets_data.get(testset_name, {})
        raw_cases = set_info.get("cases", [])
        cases = []

        for case in raw_cases:
            cid = case.get("id", "")
            case["status"] = result_map.get(cid, "-")
            cases.append(case)

        details.append({
            "name": testset_name,
            "info": set_info.get("info", ""),
            "cases": cases
        })

    return render_template("detail.html", auftrag_id=auftrag_id, events=events, details=details)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
