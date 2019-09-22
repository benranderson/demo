import os
import click

from app import create_app, db
from app.models import Job

env = os.getenv("FLASK_ENV") or "dev"
print(f"Active environment: * {env} *")
app = create_app(env)


@app.cli.command()
def recreate_db():
    """Recreate database."""
    print("Recreating database.")
    db.drop_all()
    db.create_all()
    db.session.commit()


# @app.cli.command()
# def seed():
#     """Seeds the database."""
#     print("Seeding database.")
#     job = Job(name="Seed Job", description="Just a seed job")
#     db.session.add(job)
#     db.session.commit()
