from flask import Blueprint, request, jsonify
from models import db, TriggerEvent
from datetime import datetime
from timing_config import TIMINGS

auftrag_bp = Blueprint("auftrag", __name__)

@auftrag_bp.route("/auftrag", methods=["POST"])
def auftrag():
    data = request.get_json()
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
                status="open",
            )
            db.session.add(event)
            created.append(f"{typ} → {planned_time}")

        db.session.commit()
        return jsonify({"message": "Trigger erstellt", "entries": created}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
