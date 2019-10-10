import json

from tests.utils import add_user, recreate_db


class TestUsersList:
    def test_add_user(self, client, test_db):
        response = client.post(
            "/users",
            data=json.dumps({"username": "ben", "email": "ben@email.com"}),
            content_type="application/json",
        )
        assert response.status_code == 201
        assert "ben@email.com was added!" in response.json["message"]
        assert "success" in response.json["status"]

    def test_add_user_invalid_json(self, client, test_db):
        resp = client.post(
            "/users", data=json.dumps({}), content_type="application/json"
        )
        data = json.loads(resp.data.decode())
        assert resp.status_code == 400
        assert "Invalid payload." in data["message"]
        assert "fail" in data["status"]

    def test_add_user_invalid_json_keys(self, client, test_db):
        resp = client.post(
            "/users",
            data=json.dumps({"email": "abi@email.com"}),
            content_type="application/json",
        )
        data = json.loads(resp.data.decode())
        assert resp.status_code == 400
        assert "Invalid payload." in data["message"]
        assert "fail" in data["status"]

    def test_add_user_duplicate_email(self, client, test_db):
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

    def test_remove_user(self, client, test_db):
        recreate_db()
        user = add_user("user-to-be-removed", "remove-me@email.io")
        resp_one = client.get("/users")
        data = json.loads(resp_one.data.decode())
        assert resp_one.status_code == 200
        assert len(data["data"]["users"]) == 1
        resp_two = client.delete(f"/users/{user.id}")
        data = json.loads(resp_two.data.decode())
        assert resp_two.status_code == 200
        assert "remove-me@email.io was removed!" in data["message"]
        assert "success" in data["status"]
        resp_three = client.get("/users")
        data = json.loads(resp_three.data.decode())
        assert resp_three.status_code == 200
        assert len(data["data"]["users"]) == 0

    def test_remove_user_incorrect_id(self, client, test_db):
        resp = client.delete("/users/999")
        data = json.loads(resp.data.decode())
        assert resp.status_code == 404
        assert "User does not exist" in data["message"]
        assert "fail" in data["status"]


class TestUsers:
    def test_single_user(self, client, test_db):
        user = add_user("tom", "tom@email.com")
        resp = client.get(f"/users/{user.id}")
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert "tom" in data["data"]["username"]
        assert "tom@email.com" in data["data"]["email"]
        assert "success" in data["status"]

    def test_single_user_no_id(self, client, test_db):
        resp = client.get("/users/blah")
        data = json.loads(resp.data.decode())
        assert resp.status_code == 404
        assert "User does not exist" in data["message"]
        assert "fail" in data["status"]

    def test_single_user_incorrect_id(self, client, test_db):
        resp = client.get("/users/999")
        data = json.loads(resp.data.decode())
        assert resp.status_code == 404
        assert "User does not exist" in data["message"]
        assert "fail" in data["status"]

    def test_all_users(self, client, test_db):
        recreate_db()
        add_user("michael", "michael@mherman.org")
        add_user("fletcher", "fletcher@notreal.com")
        resp = client.get("/users")
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert len(data["data"]["users"]) == 2
        assert "michael" in data["data"]["users"][0]["username"]
        assert "michael@mherman.org" in data["data"]["users"][0]["email"]
        assert "fletcher" in data["data"]["users"][1]["username"]
        assert "fletcher@notreal.com" in data["data"]["users"][1]["email"]
        assert "success" in data["status"]
