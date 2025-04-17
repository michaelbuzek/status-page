from flask import Blueprint, request, jsonify
from models import db, TriggerEvent


api_bp = Blueprint('api', __name__)

@api_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "setup_name": u.setup_name,
            "cpe": u.cpe,
            "wlan": u.wlan,
            "setup_type": u.setup_type
        } for u in users
    ])

@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        name=data.get("name"),
        email=data.get("email"),
        setup_name=data.get("setup_name"),
        cpe=data.get("cpe"),
        wlan=data.get("wlan"),
        setup_type=data.get("setup_type")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "id": user.id}), 201

# Einzelnes Event löschen
@api_bp.route("/event/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = TriggerEvent.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": f"Event {event_id} gelöscht"}), 200
    else:
        return jsonify({"error": "Event nicht gefunden"}), 404

# Alle Events zu einer Auftrag-ID löschen
@api_bp.route("/events/auftrag/<int:auftrag_id>", methods=["DELETE"])
def delete_auftrag_events(auftrag_id):
    events = TriggerEvent.query.filter_by(auftrag_id=auftrag_id).all()
    if events:
        for event in events:
            db.session.delete(event)
        db.session.commit()
        return jsonify({"message": f"Alle Events mit Auftrag-ID {auftrag_id} gelöscht"}), 200
    else:
        return jsonify({"error": "Keine Events mit dieser Auftrag-ID gefunden"}), 404
