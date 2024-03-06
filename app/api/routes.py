from app import app, models
from flask import jsonify, request, Blueprint
from app.users.utils import clear_user_table
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from app.models import User, UserSchema

api = Blueprint('api', __name__)

CORS(app)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.errorhandler(HTTPException)
def missing_parameter(e):
    return jsonify(message="Missing required parameter.", status=602), 602

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(message="Unable to locate requested resource.", status=404), 404

@app.errorhandler(401)
def unauthorized(e):
    return jsonify(message="Unauthorized to access this resource", status_code=401), 401

@app.route('/api/users/clear')
def clear_user_data():
    api_key = request.args.get('api_key')

    if api_key is None:
        return missing_parameter('Missing required parameter.')
        
    if api_key == app.config.get('API_ADMIN_KEY'):
        try:
            clear_user_table()
            return jsonify(status_code=200, content={'message': 'Succesfully cleared user database.'})
        except SQLAlchemyError as error:
            return jsonify(status_code=200, content={'message': 'Error encountered trying to clear user table.' + str(error)})
        
    else:
        return unauthorized('Unautorized access attempted.')
    
@app.route('/api/users/dump')
def dump_user_table():
    api_key = request.args.get('api_key')

    if api_key is None:
        return missing_parameter('Missing required parameter.')
    
    if api_key == app.config.get('API_ADMIN_KEY') or api_key == app.config.get('API_READ_KEY'):
        try:
            users = User.query.all()
            results = []
            for user in users:
                user.phone = str(user.phone)
                results.append(user)
            data = users_schema.dump(results)
            return jsonify(status_code=200, result=data)
        except SQLAlchemyError as error:
            return jsonify(status_code=200, content={'message': 'Error encountered trying to read user table.' + str(error)})
        
    else:
        return unauthorized('Unauthorized access attempt.')
    
@app.route('/api/users/<lname>/dump')
def dump_users_by_lname(lname):
    api_key = request.args.get('api_key')

    if api_key is None:
        return missing_parameter('Missing required parameter.')

    if api_key == app.config.get('API_ADMIN_KEY') or api_key == app.config.get('API_READ_KEY'):
        try:
            lname = lname.capitalize()
            users = User.query.filter_by(lname=lname).all()
            results = []
            if users is not None:
                for user in users:
                    user.phone = str(user.phone)
                    results.append(user)
                data = users_schema.dump(results)
                return jsonify(status_code=200, result=data)
            else:
                return jsonify(status_code=200, content={'message': 'no user by that name found'})
        except SQLAlchemyError as error:
            return jsonify(status_code=500, content={'message': 'Error encountered trying to read user table.' + str(error)})
        
    else:
        return unauthorized('Unauthorized access attempt.')