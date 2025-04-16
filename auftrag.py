# version MI 19-40
from flask import Blueprint, request, jsonify
from models import db, TriggerEvent
from datetime import datetime
from time_utils import calculate_event_times  # ⬅️ NEU

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

        # ⬇️ Nutze zentrale Berechnungslogik
        calculated_times = calculate_event_times(base_time)

        created = []
        for typ, execute_at in calculated_times.items():
            event = TriggerEvent(
                auftrag_id=auftrag_id,
                type=typ.replace("_time", ""),  # "setup_check_time" → "setup-check"
                execute_at=execute_at,
                setup=setup,
                firmware=firmware,
                router=router,
                testsets=testsets,
                status="open"
            )
            db.session.add(event)
            created.append(f"{event.type} → {execute_at.strftime('%Y-%m-%d %H:%M:%S')}")

        db.session.commit()
        print("[AUFTRAG] Erstellt:", created)
        return jsonify({"message": "Trigger erstellt", "entries": created}), 201

    except Exception as e:
        print("[AUFTRAG] Fehler:", str(e))
        return jsonify({"error": "Fehler beim Erstellen", "details": str(e)}), 400
