from demo import db
from demo.api.jobs.models import Job
from demo.api.users.models import User


def recreate_db():
    db.session.remove()
    db.drop_all()
    db.create_all()


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def add_pds_job(id, name, description):
    pds_job = Job(id=id, name=name, description=description)
    db.session.add(pds_job)
    db.session.commit()
    return pds_job
