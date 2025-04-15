#version 08:33
from flask import Blueprint, request, jsonify
from models import db

status_bp = Blueprint('status_bp', __name__)

@status_bp.route('/event-status-update', methods=['POST'])
def update_event_status():
    try:
        data = request.get_json()
        event_id = data.get("event_id")
        new_status = data.get("status")
        result_log = data.get("result_log", None)
        report_url = data.get("report_url", None)

        if not event_id or not new_status:
            return jsonify({"error": "event_id and status are required"}), 400

        update_query = '''
            UPDATE trigger_events
            SET status = %s,
                result_log = COALESCE(%s, result_log),
                report_url = COALESCE(%s, report_url),
                updated_at = NOW()
            WHERE id = %s
            RETURNING id;
        '''
        result = db.session.execute(update_query, (new_status, result_log, report_url, event_id))
        db.session.commit()

        if result.rowcount == 0:
            return jsonify({"error": "Event not found"}), 404

        return jsonify({"message": "Status updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
