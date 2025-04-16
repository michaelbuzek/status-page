from flask import Flask, render_template
from models import db, TriggerEvent
from api import api_bp
from auftrag import auftrag_bp
from event_status_update import status_bp

app = Flask(__name__)

# DB-Verbindung zu Render
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://meineapiuser:gk2u1YcUpTDkqVlhZY0U0qAtGcBWxXcD@dpg-cvrvbcur433s73eaj0k0-a.oregon-postgres.render.com/meineapidb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Blueprints registrieren
app.register_blueprint(api_bp)
app.register_blueprint(auftrag_bp)
app.register_blueprint(status_bp)

@app.route("/")
def index():
    events = TriggerEvent.query.order_by(TriggerEvent.auftrag_id, TriggerEvent.type).all()

    auftrags_map = {}
    for event in events:
        aid = event.auftrag_id
        if aid not in auftrags_map:
            auftrags_map[aid] = {
                "auftrag_id": aid,
                "router": event.router,
                "setup": event.setup,
                "firmware": event.firmware,
                "times": {},
                "status": event.status,
                "report_url": event.report_url
            }
        auftrags_map[aid]["times"][event.type] = event.execute_at

    return render_template_
