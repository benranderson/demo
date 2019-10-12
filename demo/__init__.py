import os

import rq
from flask import Flask, jsonify
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
admin = Admin(template_mode="bootstrap3")


def create_app(env=None):
    """Create a Flask application using the app factory pattern."""

    # instantiate the app
    app = Flask(__name__)

    # set config
    from demo.config import config_by_name

    app.config.from_object(config_by_name[env or "test"])

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    # configure redis
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queue = rq.Queue(app.config["QUEUE"], connection=app.redis)

    # register blueprints
    from demo.api.ping import ping_bp

    app.register_blueprint(ping_bp)

    from demo.main import main_bp

    app.register_blueprint(main_bp)

    from demo.api.users.views import users_bp

    app.register_blueprint(users_bp)

    from demo.api.jobs.views import jobs_bp

    app.register_blueprint(jobs_bp)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    # health check end point
    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
