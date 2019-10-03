import json


def test_ping(client):
    resp = client.get("/api/ping")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "pong" in data["message"]
    assert "success" in data["status"]
