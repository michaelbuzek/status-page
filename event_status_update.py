from flask import Blueprint, request, jsonify

status_bp = Blueprint('status', __name__)

@status_bp.route('/event-status-update', methods=['POST'])
def update_event_status():
    data = request.get_json()
    event_id = data.get("event_id")
    status = data.get("status")
    result_log = data.get("result_log")
    report_url = data.get("report_url")

    if not event_id or not status:
        return jsonify({"error": "event_id and status required"}), 400

    print(f"[EVENT UPDATE] ID: {event_id} | Status: {status}")
    if result_log:
        print(f"Result Log: {result_log}")
    if report_url:
        print(f"Report: {report_url}")

    return jsonify({"message": "Status updated"}), 200
