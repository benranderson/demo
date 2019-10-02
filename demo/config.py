import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(__file__).parent.absolute()
load_dotenv(basedir / ".env")


class BaseConfig:
    NAME = "base"
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    QUEUE = "demo-jobs"


class DevelopmentConfig(BaseConfig):
    NAME = "development"
    DEBUG = True
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "dev secret key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{basedir}/data-dev.sqlite"
    )


class TestingConfig(BaseConfig):
    NAME = "test"
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "test secret key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_TEST_URL", f"sqlite:///{basedir}/data-test.sqlite"
    )


class ProductionConfig(BaseConfig):
    NAME = "prod"
    DEBUG = False
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "prod secret key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{basedir}/data-prod.sqlite"
    )


EXPORT_CONFIGS = [DevelopmentConfig, TestingConfig, ProductionConfig]
config_by_name = {cfg.NAME: cfg for cfg in EXPORT_CONFIGS}
