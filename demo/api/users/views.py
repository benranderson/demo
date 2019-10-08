from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from demo import db
from demo.api.users.models import User


users_bp = Blueprint("users", __name__)
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


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<user_id>")