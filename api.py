from flask import Blueprint, request, jsonify
from models import db, TriggerEvent, TestResult

api_bp = Blueprint('api', __name__)

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

# Alle Events abrufen
@api_bp.route('/events', methods=['GET'])
def list_events():
    events = TriggerEvent.query.order_by(TriggerEvent.auftrag_id, TriggerEvent.execute_at).all()
    return jsonify([
        {
            "id": e.id,
            "auftrag_id": e.auftrag_id,
            "type": e.type,
            "execute_at": e.execute_at.isoformat(),
            "setup": e.setup,
            "firmware": e.firmware,
            "router": e.router,
            "testsets": e.testsets,
            "status": e.status,
            "result_log": e.result_log,
            "report_url": e.report_url
        } for e in events
    ])

# Neue Testergebnisse speichern
@api_bp.route("/api/resultat", methods=["POST"])
def speichere_testresultate():
    data = request.get_json()
    auftrag_id = data.get("auftrag_id")
    results = data.get("results", [])

    if not auftrag_id or not results:
        return jsonify({"error": "auftrag_id oder results fehlen"}), 400

    for result in results:
        case_id = result.get("case_id")
        status = result.get("status", "unknown")
        if case_id:
            test_result = TestResult(auftrag_id=auftrag_id, case_id=case_id, status=status)
            db.session.add(test_result)

    db.session.commit()
    return jsonify({"message": f"{len(results)} Resultate gespeichert für Auftrag {auftrag_id}."}), 200
