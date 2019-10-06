import os
import subprocess

import sys
import unittest

import click
import redis
from rq import Connection, Worker
from flask.cli import FlaskGroup

from demo import create_app, db

env = os.getenv("FLASK_ENV") or "development"
print(f"Active environment: * {env} *")
app = create_app(env)
# cli = FlaskGroup(app)


@app.cli.command()
@click.option("-c", "--cover", is_flag=True, help="Run with coverage report.")
def test(cover):
    """Run the tests with or without coverage."""
    if cover:
        cmd = "pytest --cov=src/"
        print("Running tests with coverage.")
    else:
        cmd = "pytest"
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


# @app.cli.command()
# def seed():
#     """Seeds the database."""
#     print("Seeding database.")
#     job = Job(name="Seed Job", description="Just a seed job")
#     db.session.add(job)
#     db.session.commit()


# if __name__ == "__main__":
#     cli()
