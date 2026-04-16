from app.extensions import db
from app.models import User, UserRole


def test_register_creates_user_with_hash(client, app):
    response = client.post(
        "/api/auth/register",
        json={"username": "joao", "password": "SenhaForte123"},
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["user"]["role"] == UserRole.USER.value

    with app.app_context():
        user = User.query.filter_by(username="joao").first()
        assert user is not None
        assert user.password_hash != "SenhaForte123"
        assert user.password_hash.startswith("$2")


def test_register_duplicate_username_returns_409(client):
    client.post("/api/auth/register", json={"username": "joao", "password": "SenhaForte123"})
    response = client.post("/api/auth/register", json={"username": "joao", "password": "SenhaForte123"})
    assert response.status_code == 409


def test_login_me_logout_flow(client):
    client.post("/api/auth/register", json={"username": "user1", "password": "SenhaForte123"})

    login_resp = client.post("/api/auth/login", json={"username": "user1", "password": "SenhaForte123"})
    assert login_resp.status_code == 200

    me_resp = client.get("/api/auth/me")
    assert me_resp.status_code == 200
    assert me_resp.get_json()["user"]["username"] == "user1"

    logout_resp = client.post("/api/auth/logout")
    assert logout_resp.status_code == 200

    me_after_logout = client.get("/api/auth/me")
    assert me_after_logout.status_code == 401


def test_invalid_login_returns_401(client):
    client.post("/api/auth/register", json={"username": "user2", "password": "SenhaForte123"})
    response = client.post("/api/auth/login", json={"username": "user2", "password": "wrong-pass"})
    assert response.status_code == 401


def test_user_cannot_access_admin_routes(client):
    client.post("/api/auth/register", json={"username": "user3", "password": "SenhaForte123"})
    client.post("/api/auth/login", json={"username": "user3", "password": "SenhaForte123"})

    list_resp = client.get("/api/users")
    assert list_resp.status_code == 403

    create_resp = client.post(
        "/api/users",
        json={"username": "new_user", "password": "SenhaForte123", "role": "USER"},
    )
    assert create_resp.status_code == 403


def test_admin_can_manage_users(client, app, admin_user):
    login_resp = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "Admin@123456"},
    )
    assert login_resp.status_code == 200

    create_resp = client.post(
        "/api/users",
        json={"username": "cliente", "password": "Cliente@123", "role": "USER"},
    )
    assert create_resp.status_code == 201
    created_user_id = create_resp.get_json()["user"]["id"]

    patch_resp = client.patch(f"/api/users/{created_user_id}", json={"role": "ADMIN", "is_active": False})
    assert patch_resp.status_code == 200
    patched_payload = patch_resp.get_json()["user"]
    assert patched_payload["role"] == "ADMIN"
    assert patched_payload["is_active"] is False

    delete_resp = client.delete(f"/api/users/{created_user_id}")
    assert delete_resp.status_code == 200

    with app.app_context():
        user = db.session.get(User, created_user_id)
        assert user is None
