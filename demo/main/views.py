from flask import render_template, request, current_app, jsonify

from demo import db
from demo.main import main_bp
from demo.api.jobs.models import Job


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    time = int(data.get("time"))
    rq_job = current_app.task_queue.enqueue("app.jobs." + name, time)
    job = Job(id=rq_job.get_id(), name=name, description=description)
    db.session.add(job)
    db.session.commit()
    return job.to_dict(), 201


@main_bp.route("/jobs")
def get_jobs_in_progress():
    jobs = Job.query.filter_by(complete=False).all()
    return jsonify({"jobs": [job.to_dict() for job in jobs], "count": len(jobs)})


@main_bp.route("/jobs/<id>")
def get_job(id):
    job = Job.query.filter_by(id=id).first_or_404()
    return jsonify(job.to_dict())
