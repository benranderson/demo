import pytest

from demo import create_app
from demo import db as _db


@pytest.fixture(scope="session")
def app():
    """Setup flask test app, this only gets executed once."""
    _app = create_app("test")
    with _app.app_context():
        yield _app


@pytest.fixture
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
