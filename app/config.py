import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(__file__).parent.absolute()
load_dotenv(basedir / ".env")


class BaseConfig:
    NAME = "base"
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    NAME = "dev"
    DEBUG = True
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "dev secret key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app-dev.db"


class TestingConfig(BaseConfig):
    NAME = "test"
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "testing secret key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app-test.db"


class ProductionConfig(BaseConfig):
    NAME = "prod"
    DEBUG = False
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "prod secret key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app-prod.db"


EXPORT_CONFIGS = [DevelopmentConfig, TestingConfig, ProductionConfig]
config_by_name = {cfg.NAME: cfg for cfg in EXPORT_CONFIGS}
