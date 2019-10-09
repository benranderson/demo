from flask import jsonify, request
from flask_restful import Api, Resource, reqparse

from demo import db
from demo.api.jobs.models import Job
from demo.api.jobs import jobs_bp

api = Api(jobs_bp)

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("description")


class Jobs(Resource):
    def get(self, job_id):
        """Get single job details"""
        job = Job.query.get_or_404(job_id)
        return jsonify(job.to_dict())


class JobsList(Resource):
    def get(self):
        """Get all jobs"""
        jobs = Job.query.all()
        return jsonify({"jobs": [job.to_dict() for job in jobs], "count": len(jobs)})

    def post(self):
        """Create a new job"""
        data = request.get_json()
        job = Job()
        job.from_dict(data)
        db.session.add(job)
        db.session.commit()
        return job.to_dict(), 201


# setup API resource routing
api.add_resource(JobsList, "/jobs")
api.add_resource(Jobs, "/jobs/<job_id>")
