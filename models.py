from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    setup_name = db.Column(db.String(100))
    cpe = db.Column(db.String(100))
    wlan = db.Column(db.String(100))
    setup_type = db.Column(db.String(100))
