from flask import Blueprint, request, jsonify
from models import db, TriggerEvent
from datetime import datetime

auftrag_bp = Blueprint('auftrag', __name__)

@auftrag_bp.route('/auftrag', methods=['POST'])
def auftrag():
    data = request.get_json()
    print(f"[AUFTRAG] Eingehend: {data}")

    try:
        new_event = TriggerEvent(
            auftrag_id=data["auftrag_id"],
            type=data["type"],
            execute_at=datetime.fromisoformat(data["execute_at"]),
            setup=data.get("setup", ""),
            firmware=data.get("firmware", ""),
            router=data.get("router", ""),
            testsets=data.get("testsets", []),
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Auftrag gespeichert", "event_id": new_event.id}), 201

    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"error": "Fehler beim Speichern"}), 500
