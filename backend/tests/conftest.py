import pytest

from app import create_app
from app.extensions import db
from app.models import User, UserRole


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite+pysqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "CORS_ORIGINS": ["http://127.0.0.1:5500"],
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_user(app):
    with app.app_context():
        user = User(username="admin", role=UserRole.ADMIN.value, is_active=True)
        user.set_password("Admin@123456")
        db.session.add(user)
        db.session.commit()
        return user
