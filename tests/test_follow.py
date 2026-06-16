from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
API_KEY = "alice-key"


def _headers():
    return {"api-key": API_KEY}


def test_follow_and_unfollow_user():
    """Подписка и отписка от другого пользователя."""

    me_resp = client.get("/api/users/me", headers=_headers())
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    current_user_id = me_data["user"]["id"]

    user_id_to_follow = 21
    assert user_id_to_follow != current_user_id

    follow_resp = client.post(
        f"/api/users/{user_id_to_follow}/follow", headers=_headers()
    )
    assert follow_resp.status_code == 200
    follow_data = follow_resp.json()
    assert follow_data["result"] is True

    unfollow_resp = client.delete(
        f"/api/users/{user_id_to_follow}/follow", headers=_headers()
    )
    assert unfollow_resp.status_code == 200
    unfollow_data = unfollow_resp.json()
    assert unfollow_data["result"] is True
