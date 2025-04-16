from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, TriggerEvent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meineapiuser:gk2u1YcUpTDkqVlhZY0U0qAtGcBWxXcD@dpg-cvrvbcur433s73eaj0k0-a.oregon-postgres.render.com/meineapidb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    events = TriggerEvent.query.order_by(TriggerEvent.execute_at).all()
    return render_template('status.html', events=events)

@app.route('/admin')
def admin():
    events = TriggerEvent.query.order_by(TriggerEvent.execute_at).all()
    return render_template('admin.html', events=events)

@app.route('/event-status-update', methods=['POST'])
def update_status():
    data = request.get_json()
    event_id = data.get('event_id')
    event = TriggerEvent.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    if 'status' in data:
        event.status = data['status']
    if 'result_log' in data:
        event.result_log = data['result_log']
    if 'report_url' in data:
        event.report_url = data['report_url']

    db.session.commit()
    return jsonify({"message": "Status updated"}), 200

if __name__ == '__main__':
    app.run(debug=True)
