import os
from pathlib import Path

basedir = Path(__file__).parent.absolute()


class BaseConfig:
    NAME = "base"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    NAME = "dev"
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "dev secret key")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app-dev.db"


class TestingConfig(BaseConfig):
    NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "testing secret key")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app-test.db"


class ProductionConfig(BaseConfig):
    NAME = "prod"
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "prod secret key")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app-prod.db"


EXPORT_CONFIGS = [DevelopmentConfig, TestingConfig, ProductionConfig]
config_by_name = {cfg.NAME: cfg for cfg in EXPORT_CONFIGS}
