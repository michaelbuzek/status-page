from flask import Blueprint, request, jsonify
from models import db, TriggerEvent, TestResult, User

api_bp = Blueprint('api', __name__)

# ---------------- USERS ----------------

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

# ---------------- EVENTS ----------------

@api_bp.route("/event/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = TriggerEvent.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": f"Event {event_id} gelöscht"}), 200
    else:
        return jsonify({"error": "Event nicht gefunden"}), 404

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

# ---------------- TEST RESULTS ----------------

@api_bp.route("/resultat", methods=["POST"])
def empfange_resultate():
    data = request.get_json()
    auftrag_id = data.get("auftrag_id")
    results = data.get("results", [])

    if not auftrag_id or not results:
        return jsonify({"error": "auftrag_id oder results fehlen"}), 400

    for result in results:
        case_id = result.get("case_id")
        status = result.get("status")

        if case_id and status:
            db.session.execute(
                """
                INSERT INTO test_results (auftrag_id, case_id, status)
                VALUES (:auftrag_id, :case_id, :status)
                """,
                {"auftrag_id": auftrag_id, "case_id": case_id, "status": status}
            )

    db.session.commit()
    return jsonify({"message": "Results saved"}), 200
