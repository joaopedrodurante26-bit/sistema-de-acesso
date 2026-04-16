from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..models import User, UserRole

auth_bp = Blueprint("auth", __name__)


def _validate_credentials(data):
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username:
        return None, None, "Username is required"
    if len(username) < 3:
        return None, None, "Username must have at least 3 characters"
    if not password:
        return None, None, "Password is required"
    if len(password) < 8:
        return None, None, "Password must have at least 8 characters"
    return username, password, None


@auth_bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    username, password, error = _validate_credentials(payload)
    if error:
        return jsonify({"error": error}), 400

    user = User(username=username, role=UserRole.USER.value, is_active=True)
    user.set_password(password)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username already exists"}), 409

    return jsonify({"message": "User created", "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    if not user.is_active:
        return jsonify({"error": "User is inactive"}), 403

    login_user(user)
    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.get("/me")
@login_required
def me():
    return jsonify({"user": current_user.to_dict()}), 200
