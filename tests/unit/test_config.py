import os


def test_development_config(app):
    app.config.from_object("demo.config.DevelopmentConfig")
    assert app.config["SECRET_KEY"] == "dev secret key"
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")


def test_testing_config(app):
    app.config.from_object("demo.config.TestingConfig")
    assert app.config["SECRET_KEY"] == "test secret key"
    assert app.config["TESTING"]
    assert not app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_TEST_URL")


def test_production_config(app):
    app.config.from_object("demo.config.ProductionConfig")
    assert app.config["SECRET_KEY"] == "prod secret key"
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
