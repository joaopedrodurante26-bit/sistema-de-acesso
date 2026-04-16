from flask import Flask, jsonify

from .cli import register_cli_commands
from .config import Config
from .extensions import cors, db, login_manager, migrate
from .models import User


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    _init_extensions(app)
    _register_blueprints(app)
    _register_handlers(app)
    register_cli_commands(app)

    return app


def _init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )


def _register_blueprints(app):
    from .auth.routes import auth_bp
    from .core.routes import core_bp
    from .users.routes import users_bp

    app.register_blueprint(core_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")


def _register_handlers(app):
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "Authentication required"}), 401

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify({"error": "Internal server error"}), 500
