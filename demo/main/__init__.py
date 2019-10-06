from flask import Blueprint

main_bp = Blueprint("main", __name__)

from demo.main import views
