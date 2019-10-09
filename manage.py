import os
import subprocess

import click
import redis
from rq import Connection, Worker

from demo import create_app, db
from demo.api.users.models import User

env = os.getenv("FLASK_ENV") or "development"
print(f"Active environment: * {env} *")
app = create_app(env)


@app.cli.command()
@click.option("-c", "--cover", is_flag=True, help="Run with coverage report.")
def test(cover):
    """Run the tests with or without coverage."""
    if cover:
        cmd = "pytest -p no:warnings --cov=demo/ --cov-report html"
        print("Running tests with coverage.")
    else:
        cmd = "pytest -p no:warnings"
        print("Running tests.")
    return subprocess.run(cmd, shell=True)


@app.cli.command()
def recreate_db():
    """Recreate database."""
    print("Recreating database.")
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command()
def run_worker():
    redis_url = app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config["QUEUE"])
        worker.work()


@app.cli.command()
def seed_db():
    """Seeds the database."""
    print("Seeding database.")
    db.session.add(User(username="ben", email="ben@email.com"))
    db.session.add(User(username="benranderson", email="ben@email.org"))
    db.session.commit()
