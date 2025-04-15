from flask import Blueprint, request, jsonify
from models import db, User

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
