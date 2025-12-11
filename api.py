from flask import Blueprint, jsonify, request, session
from models import db, User, Device, Event
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')

# 🧩 User Module: Login
@api.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        session['user'] = user.username
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Invalid credentials"}), 401

# 🧩 Database + Surveillance: List devices
@api.route('/devices')
def devices():
    return jsonify([{"id": d.id, "name": d.name, "type": d.device_type, "status": d.status} for d in Device.query.all()])

# 🧩 Safety & Alert Module: Post an alert (used by simulator)
# inside api.py add_event
@api.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    e = Event(
        device_name=data.get('device_name'),
        event_type=data.get('event_type'),
        message=data.get('message'),
        temperature=data.get('temperature'),
        humidity=data.get('humidity')
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({"ok": True})


# 🧩 Retrieve recent events
# inside api.py get_events (return newest first)
@api.route('/events')
def get_events():
    events = Event.query.order_by(Event.timestamp.desc()).limit(50).all()
    return jsonify([{
        "device_name": e.device_name,
        "event_type": e.event_type,
        "message": e.message,
        "timestamp": e.timestamp.isoformat(),
        "temperature": e.temperature,
        "humidity": e.humidity
    } for e in events])

# 🧩 Device control simulation
@api.route('/device/<int:id>/control', methods=['POST'])
def control_device(id):
    data = request.json
    d = Device.query.get(id)
    if d:
        d.status = data.get('action', d.status)
        db.session.commit()
        return jsonify({"ok": True, "status": d.status})
    return jsonify({"ok": False, "error": "Device not found"}), 404
