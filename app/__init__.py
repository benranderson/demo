from flask import Flask, jsonify
from flask.cli import FlaskGroup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(env=None):
    """Create a Flask application using the app factory pattern."""

    # instantiate the app
    app = Flask(__name__)

    # set config
    from app.config import config_by_name

    app.config.from_object(config_by_name[env or "test"])

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.api.routes import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        from app.models import Job

        return {"app": app, "db": db, "Job": Job}

    # health check end point
    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
