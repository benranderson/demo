from flask import Blueprint

bp = Blueprint("main", __name__)

from demo.main import routes
