from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TriggerEvent(db.Model):
    __tablename__ = 'trigger_events'

    id = db.Column(db.Integer, primary_key=True)
    auftrag_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Text, nullable=False)  # setup-check, fw-download, run-test
    execute_at = db.Column(db.DateTime, nullable=False)
    setup = db.Column(db.Text)
    firmware = db.Column(db.Text)
    router = db.Column(db.Text)
    testsets = db.Column(db.ARRAY(db.Text))  # z. B. ['wlan', 'security']
    status = db.Column(db.Text, default='open')  # open, running, done, error
    result_log = db.Column(db.Text)
    report_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
