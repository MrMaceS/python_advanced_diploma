from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
API_KEY = "alice-key"


def _headers():
    return {"api-key": API_KEY}


def test_get_tweets_ok():
    """GET /api/tweets — успешный ответ и наличие списка твитов."""
    response = client.get("/api/tweets", headers=_headers())
    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True
    assert "tweets" in data
    assert isinstance(data["tweets"], list)


def test_create_tweet_and_see_in_feed():
    """Создаём твит и убеждаемся, что API возвращает его id."""
    payload = {"tweet_data": "Тестовый твит из pytest"}
    response = client.post("/api/tweets", headers=_headers(), json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True
    assert "tweet_id" in data
    assert isinstance(data["tweet_id"], int)


def test_like_and_unlike_tweet():
    """Лайк/анлайк твита по id из ленты."""

    feed_resp = client.get("/api/tweets", headers=_headers())
    assert feed_resp.status_code == 200
    feed_data = feed_resp.json()
    assert feed_data["result"] is True
    assert feed_data["tweets"], "Лента пустая, нечего лайкать"

    tweet_id = feed_data["tweets"][0]["id"]

    like_resp = client.post(f"/api/tweets/{tweet_id}/likes", headers=_headers())
    assert like_resp.status_code == 200
    like_data = like_resp.json()
    assert like_data["result"] is True

    unlike_resp = client.delete(f"/api/tweets/{tweet_id}/likes", headers=_headers())
    assert unlike_resp.status_code == 200
    unlike_data = unlike_resp.json()
    assert unlike_data["result"] is True


def test_delete_own_tweet():
    """Создаём твит и удаляем его, проверяя успешный результат."""
    payload = {"tweet_data": "Твит для удаления"}
    create_resp = client.post("/api/tweets", headers=_headers(), json=payload)
    assert create_resp.status_code == 200
    data = create_resp.json()
    tweet_id = data["tweet_id"]

    delete_resp = client.delete(f"/api/tweets/{tweet_id}", headers=_headers())
    assert delete_resp.status_code == 200
    delete_data = delete_resp.json()
    assert delete_data["result"] is True


def test_upload_media_ok(tmp_path):
    """Загрузка файла через /api/medias."""

    file_content = b"test-bytes"
    files = {"file": ("test.jpg", file_content, "image/jpeg")}

    resp = client.post("/api/medias", headers=_headers(), files=files)
    assert resp.status_code == 200

    data = resp.json()
    assert data["result"] is True
    assert "media_id" in data
