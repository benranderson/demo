from flask_restplus import Namespace, Resource, fields

from .model import DAO

api = Namespace("API", description="REST API")

job = api.model(
    "Job",
    {
        "id": fields.Integer(readonly=True, description="The job unique identifier"),
        "calculation": fields.String(
            required=True, description="The calculation details"
        ),
    },
)


@api.route("/")
class JobList(Resource):
    """Shows a list of all jobs, and lets you POST to add new jobs."""

    @api.doc("list_jobs")
    @api.marshal_list_with(job)
    def get(self):
        """Get all jobs"""
        return DAO.jobs

    @api.doc("create_job")
    @api.expect(job)
    @api.marshal_with(job, code=201)
    def post(self):
        """Create a new job"""
        return DAO.create(api.payload), 201


@api.route("/<int:id>")
@api.response(404, "Job not found")
@api.param("id", "The job identifier")
class Job(Resource):
    """Show, delete or update a single job"""

    @api.doc("get_job")
    @api.marshal_with(job)
    def get(self, id):
        """Fetch a given job"""
        return DAO.get(id)

    @api.doc("delete_job")
    @api.response(204, "Job deleted")
    def delete(self, id):
        """Delete a job given its identifier"""
        DAO.delete(id)
        return "", 204

    @api.expect(job)
    @api.marshal_with(job)
    def put(self, id):
        """Update a job given its identifier"""
        return DAO.update(id, api.payload)
