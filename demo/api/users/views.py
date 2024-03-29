from flask import request
from flask_restful import Api, Resource
from sqlalchemy import exc

from demo import db
from demo.api.users import users_bp
from demo.api.users.models import User

api = Api(users_bp)


class UsersList(Resource):
    def post(self):
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            return response_object, 400
        username = post_data.get("username")
        email = post_data.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400
        try:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object["status"] = "success"
            response_object["message"] = f"{email} was added!"
            return response_object, 201
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400

    def get(self):
        response_object = {
            "status": "success",
            "data": {"users": [user.to_json() for user in User.query.all()]},
        }
        return response_object, 200


class Users(Resource):
    def get(self, user_id):
        response_object = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.query.filter_by(id=int(user_id)).first()
        except ValueError:
            return response_object, 404
        if not user:
            return response_object, 404
        response_object = {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "active": user.active,
            },
        }
        return response_object, 200

    def put(self, user_id):
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            return response_object, 400
        username = post_data.get("username")
        email = post_data.get("email")
        if not username or not email:
            return response_object, 400
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                response_object["message"] = "User does not exist."
                return response_object, 404
            user.username = username
            user.email = email
            db.session.commit()
            response_object["status"] = "success"
            response_object["message"] = f"{user.id} was updated!"
            return response_object, 200
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400

    def delete(self, user_id):
        response_object = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.query.filter_by(id=int(user_id)).first()
        except ValueError:
            return response_object, 404
        if not user:
            return response_object, 404
        db.session.delete(user)
        db.session.commit()
        response_object["status"] = "success"
        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<user_id>")
