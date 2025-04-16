from flask import Blueprint, request, jsonify
from models import db, TriggerEvent
from datetime import datetime
from timing_config import TIMINGS

auftrag_bp = Blueprint('auftrag', __name__)

@auftrag_bp.route('/auftrag', methods=['POST'])
def auftrag():
    data = request.get_json()
    print(f"[AUFTRAG] Eingehend: {data}")

    try:
        base_time = datetime.fromisoformat(data["execute_at"])
        auftrag_id = data["auftrag_id"]
        router = data["router"]
        setup = data["setup"]
        firmware = data["firmware"]
        testsets = data.get("testsets", [])

        event_types = ["setup-check", "fw-download", "run-test"]
        created = []

        for typ in event_types:
            planned_time = base_time + TIMINGS[typ]
            event = TriggerEvent(
                auftrag_id=auftrag_id,
                type=typ,
                execute_at=planned_time,
                setup=setup,
                firmware=firmware,
                router=router,
                testsets=testsets,
                status="open"
            )
            db.session.add(event)
            created.append(f"{typ} → {planned_time.strftime('%Y-%m-%d %H:%M:%S')}")

        db.session.commit()
        print("[AUFTRAG] Erstellt:", created)
        return jsonify({"message": "Trigger erstellt", "entries": created}), 201

    except Exception as e:
        print("[AUFTRAG] Fehler:", str(e))
        return jsonify({"error": "Fehler beim Erstellen", "details": str(e)}), 400
