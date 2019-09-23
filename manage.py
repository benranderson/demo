import os
import subprocess

import click
import redis
from rq import Connection, Worker
from flask.cli import FlaskGroup

from app import create_app, db
from app.models import Job

env = os.getenv("FLASK_ENV") or "dev"
print(f"Active environment: * {env} *")
app = create_app(env)
cli = FlaskGroup(create_app=create_app)


@cli.command()
@click.argument("path", default="tests")
def test(path):
    """Run tests with Pytest.

    :param path: Test path
    :return: Subprocess call result
    """
    cmd = f"py.test {path}"
    return subprocess.call(cmd, shell=True)


@cli.command()
def recreate_db():
    """Recreate database."""
    print("Recreating database.")
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("run_worker")
def run_worker():
    redis_url = app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config["QUEUE"])
        worker.work()


# @app.cli.command()
# def seed():
#     """Seeds the database."""
#     print("Seeding database.")
#     job = Job(name="Seed Job", description="Just a seed job")
#     db.session.add(job)
#     db.session.commit()


if __name__ == "__main__":
    cli()
