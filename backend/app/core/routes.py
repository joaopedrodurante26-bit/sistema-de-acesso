from flask import Blueprint, jsonify
from flask_login import current_user, login_required

core_bp = Blueprint("core", __name__)


@core_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@core_bp.get("/dashboard")
@login_required
def dashboard():
    return jsonify(
        {
            "message": "Access granted",
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "role": current_user.role,
            },
        }
    ), 200
