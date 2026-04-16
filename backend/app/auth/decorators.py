from functools import wraps

from flask import jsonify
from flask_login import current_user, login_required


def role_required(role):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapped(*args, **kwargs):
            if current_user.role != role:
                return jsonify({"error": "Forbidden"}), 403
            return func(*args, **kwargs)

        return wrapped

    return decorator
