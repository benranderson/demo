from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
import rq


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


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

    # configure redis
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queue = rq.Queue(app.config["QUEUE"], connection=app.redis)

    # register blueprints
    from demo.api.routes import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    from demo.main import bp as main_bp

    app.register_blueprint(main_bp)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        from demo.models import Job

        return {"app": app, "db": db, "Job": Job}

    # health check end point
    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
