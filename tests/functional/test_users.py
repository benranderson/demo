import json

from demo.api.users.models import User


def test_add_user(client, test_db):
    response = client.post(
        "/users",
        data=json.dumps({"username": "ben", "email": "ben@email.com"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert "ben@email.com was added!" in response.json["message"]
    assert "success" in response.json["status"]


def test_add_user_invalid_json(client, test_db):
    resp = client.post("/users", data=json.dumps({}), content_type="application/json")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_user_invalid_json_keys(client, test_db):
    resp = client.post(
        "/users",
        data=json.dumps({"email": "abi@email.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_user_duplicate_email(client, test_db):
    client.post(
        "/users",
        data=json.dumps({"username": "ben", "email": "ben@email.com"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "ben", "email": "ben@email.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]
    assert "fail" in data["status"]


def test_single_user(client, test_db):
    user = User(username="tom", email="tom@email.com")
    test_db.session.add(user)
    test_db.session.commit()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "tom" in data["data"]["username"]
    assert "tom@email.com" in data["data"]["email"]
    assert "success" in data["status"]


def test_single_user_no_id(client, test_db):
    resp = client.get("/users/blah")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User does not exist" in data["message"]
    assert "fail" in data["status"]


def test_single_user_incorrect_id(client, test_db):
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User does not exist" in data["message"]
    assert "fail" in data["status"]
