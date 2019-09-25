import pytest

from demo import create_app
from demo import db as _db


@pytest.yield_fixture(scope="session")
def app():
    """Setup flask test app, this only gets executed once."""
    _app = create_app("test")

    # establish an application context before running the tests
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope="function")
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope="session")
def db(app):
    """
    Setup database, this only gets executed once per session.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()
    return _db
