from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    status = db.Column(db.String(50))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100))
    event_type = db.Column(db.String(50))
    message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
