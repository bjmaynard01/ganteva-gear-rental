from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from app.api.errors import bp as errors_api

CORS(errors_api)

@errors_api.errorhandler(HTTPException)
def missing_parameter(e):
    return jsonify(message="Missing required parameter.", status=602), 602

@errors_api.errorhandler(404)
def resource_not_found(e):
    return jsonify(message="Unable to locate requested resource.", status=404), 404

@errors_api.errorhandler(401)
def unauthorized(e):
    if request.path.startswith('/api/'):
        return jsonify(message="Unauthorized to access this resource", status_code=401), 401