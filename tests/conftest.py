import pytest

from demo import create_app
from demo import db as _db


@pytest.fixture(scope="module")
def app():
    """Setup flask test app, this only gets executed once per module."""
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


@pytest.fixture(scope="module")
def test_db(app):
    """
    Setup database, this only gets executed once per module.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()
