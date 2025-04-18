from flask import Flask, render_template
from models import db, TriggerEvent
from api import api_bp
from auftrag import auftrag_bp
from event_status_update import status_bp
from time_utils import gruppiere_events_nach_auftrag
import json
from sqlalchemy import text

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

    # Lade alle Testresultate zu diesem Auftrag aus der DB
    with db.engine.connect() as conn:
        results = conn.execute(
            text("SELECT case_id, status FROM test_results WHERE auftrag_id = :aid"),
            {"aid": auftrag_id}
        ).fetchall()

    # Erstelle Dictionary: case_id → status
    result_map = {r.case_id: r.status for r in results}

    # Lade Testsets aus JSON-Datei
    with open("testsets.json", "r") as f:
        testsets_data = json.load(f)

    # Extrahiere gewählte Testsets aus Events (z. B. run-test)
    testset_namen = []
    for e in events:
        if e.type == "run-test" and e.testsets:
            testset_namen = e.testsets
            break

    # Erstelle detail-Objekt für die Anzeige
    details = []
    for testset_name in testset_namen:
        raw_cases = testsets_data.get(testset_name, [])
        cases = []

        for raw_case in raw_cases:
            # Wenn raw_case bereits ein Dict ist
            if isinstance(raw_case, dict):
                cid = raw_case.get("id", "")
                raw_case["status"] = result_map.get(cid, "-")
                cases.append(raw_case)
            else:
                # Fallback: raw_case ist nur ein String
                cases.append({
                    "id": raw_case,
                    "name": raw_case,
                    "info": "",
                    "status": result_map.get(raw_case, "-")
                })

        details.append({
            "name": testset_name,
            "testcases": cases
        })

    return render_template("detail.html", auftrag_id=auftrag_id, events=events, details=details)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
