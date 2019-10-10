import pytest

from demo.api.jobs.models import Job
from tests.utils import add_pds_job


def test_PDSJob_retrieve(test_db):
    pds_job = add_pds_job(id="id", name="Pending", description="Test job")
    p = Job.query.first()
    assert p.__dict__ == pds_job.__dict__
