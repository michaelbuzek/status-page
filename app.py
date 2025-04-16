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
    events = TriggerEvent.query.order_by(TriggerEvent.execute_at.asc()).all()
    return render_template("status.html", events=events)

@app.route("/admin")
def admin():
    events = TriggerEvent.query.order_by(TriggerEvent.execute_at).all()
    return render_template("admin.html", events=events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
