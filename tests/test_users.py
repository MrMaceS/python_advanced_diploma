from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

API_KEY = "alice-key"


def _headers():
    return {"api-key": API_KEY}


def test_get_me_ok():
    """GET /api/users/me — успешный ответ и корректная структура."""
    response = client.get("/api/users/me", headers=_headers())
    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True
    assert "user" in data

    user = data["user"]
    assert "id" in user
    assert "name" in user
    assert "followers" in user
    assert "following" in user


def test_get_user_by_id_ok():
    """GET /api/users/{id} — проверяем структуру профиля пользователя."""

    me_resp = client.get("/api/users/me", headers=_headers())
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    current_user_id = me_data["user"]["id"]

    response = client.get(f"/api/users/{current_user_id}", headers=_headers())
    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True
    assert "user" in data

    user = data["user"]
    assert "id" in user
    assert "name" in user
    assert "followers" in user
    assert "following" in user
