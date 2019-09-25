import pytest

from demo.models import Job


@pytest.fixture
def pds_job():
    return Job(id="id", name="Pending", description="Test job")


def test_PDSJob_create(pds_job):
    assert pds_job


def test_PDSJob_retrieve(pds_job, db):
    db.session.add(pds_job)
    db.session.commit()
    p = Job.query.first()
    assert p.__dict__ == pds_job.__dict__
