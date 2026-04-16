from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from flask_login import current_user

from ..auth.decorators import role_required
from ..extensions import db
from ..models import User, UserRole

users_bp = Blueprint("users", __name__)


def _parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y", "on"}:
            return True
        if normalized in {"false", "0", "no", "n", "off"}:
            return False
    return None


@users_bp.get("")
@role_required(UserRole.ADMIN.value)
def list_users():
    users = User.query.order_by(User.id.asc()).all()
    return jsonify({"users": [user.to_dict() for user in users]}), 200


@users_bp.post("")
@role_required(UserRole.ADMIN.value)
def create_user():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    role = (payload.get("role") or UserRole.USER.value).upper()
    is_active_raw = payload.get("is_active", True)
    is_active = _parse_bool(is_active_raw)
    if is_active is None:
        return jsonify({"error": "is_active must be boolean"}), 400

    if not username or len(username) < 3:
        return jsonify({"error": "Username must have at least 3 characters"}), 400
    if not password or len(password) < 8:
        return jsonify({"error": "Password must have at least 8 characters"}), 400
    if role not in (UserRole.ADMIN.value, UserRole.USER.value):
        return jsonify({"error": "Invalid role"}), 400

    user = User(username=username, role=role, is_active=is_active)
    user.set_password(password)
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username already exists"}), 409

    return jsonify({"message": "User created", "user": user.to_dict()}), 201


@users_bp.patch("/<int:user_id>")
@role_required(UserRole.ADMIN.value)
def update_user(user_id):
    payload = request.get_json(silent=True) or {}
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if "role" in payload:
        new_role = str(payload.get("role", "")).upper()
        if new_role not in (UserRole.ADMIN.value, UserRole.USER.value):
            return jsonify({"error": "Invalid role"}), 400
        user.role = new_role

    if "is_active" in payload:
        parsed_is_active = _parse_bool(payload.get("is_active"))
        if parsed_is_active is None:
            return jsonify({"error": "is_active must be boolean"}), 400
        user.is_active = parsed_is_active

    if "password" in payload:
        new_password = payload.get("password") or ""
        if len(new_password) < 8:
            return jsonify({"error": "Password must have at least 8 characters"}), 400
        user.set_password(new_password)

    db.session.commit()
    return jsonify({"message": "User updated", "user": user.to_dict()}), 200


@users_bp.delete("/<int:user_id>")
@role_required(UserRole.ADMIN.value)
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.id == current_user.id:
        return jsonify({"error": "You cannot delete your own account"}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
