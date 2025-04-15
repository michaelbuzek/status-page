from flask import Blueprint, request, jsonify
auftrag_bp = Blueprint('auftrag', __name__)

@auftrag_bp.route('/auftrag', methods=['POST'])
def auftrag():
    data = request.get_json()
    print(f"[AUFTRAG] Eingehend: {data}")
    return jsonify({"message": "Auftrag empfangen"}), 200
