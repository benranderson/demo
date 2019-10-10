from flask import Blueprint
from flask_restful import Api, Resource

ping_bp = Blueprint("ping", __name__)
api = Api(ping_bp)


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


api.add_resource(Ping, "/ping")
