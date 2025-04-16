from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TriggerEvent(db.Model):
    __tablename__ = 'trigger_events'

    id = db.Column(db.Integer, primary_key=True)
    auftrag_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Text, nullable=False)
    execute_at = db.Column(db.DateTime, nullable=False)
    setup = db.Column(db.Text)
    firmware = db.Column(db.Text)
    router = db.Column(db.Text)
    testsets = db.Column(db.ARRAY(db.Text))
    status = db.Column(db.Text, default='open')
    result_log = db.Column(db.Text)
    report_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
