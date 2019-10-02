import os
import sys
import time
from rq import get_current_job

from demo import db, create_app
from demo.models import Job

env = os.getenv("FLASK_ENV") or "development"
app = create_app(env)
app.app_context().push()


def example(seconds):
    try:
        for i in range(seconds):
            progress = 100.0 * i / seconds
            _set_task_progress(progress)
            print(f"seconds: {i}, progress: {progress}%")
            time.sleep(1)
        _set_task_progress(100)
        print("Task completed")
    except:
        _set_task_progress(100)
        app.logger.error("Unhandled exception", exc_info=sys.exc_info())


def _set_task_progress(progress):
    rq_job = get_current_job()
    if rq_job:
        rq_job.meta["progress"] = progress
        rq_job.save_meta()
        job = Job.query.get(rq_job.get_id())
        if progress >= 100:
            job.complete = True
        db.session.commit()
