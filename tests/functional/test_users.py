import json


def test_add_user(client, db):
    response = client.post(
        "/users",
        data=json.dumps({"username": "ben", "email": "ben@email.com"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert "ben@email.com was added!" in response.json["message"]
    assert "success" in response.json["status"]
