from flask import Blueprint

jobs_bp = Blueprint("jobs", __name__)

from demo.api.jobs import views
