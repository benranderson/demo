from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api

from demo import db
from demo.api.users.models import User


users_bp = Blueprint("users", __name__)
api = Api(users_bp)
