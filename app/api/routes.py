from flask import jsonify, request, current_app
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from app.models import User, UserSchema
from app.api import bp as api_bp
from app.users.utils import clear_user_table

CORS(api_bp)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api_bp.errorhandler(HTTPException)
def missing_parameter(e):
    return jsonify(message="Missing required parameter.", status=602), 602

@api_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(message="Unable to locate requested resource.", status=404), 404

@api_bp.errorhandler(401)
def unauthorized(e):
    return jsonify(message="Unauthorized to access this resource", status_code=401), 401

@api_bp.route('/api/users/clear')
def clear_user_data():
    api_key = request.args.get('api_key')

    if api_key is None:
        return missing_parameter('Missing required parameter.')
        
    if api_key == current_app.config.get('API_ADMIN_KEY'):
        try:
            clear_user_table()
            return jsonify(status_code=200, content={'message': 'Succesfully cleared user database.'})
        except SQLAlchemyError as error:
            return jsonify(status_code=200, content={'message': 'Error encountered trying to clear user table.' + str(error)})
        
    else:
        return unauthorized('Unautorized access attempted.')
    
@api_bp.route('/api/users/dump')
def dump_user_table():
    api_key = request.args.get('api_key')

    if api_key is None:
        return missing_parameter('Missing required parameter.')
    
    if api_key == current_app.config.get('API_ADMIN_KEY') or api_key == current_app.config.get('API_READ_KEY'):
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
    
@api_bp.route('/api/users/<lname>/dump')
def dump_users_by_lname(lname):
    api_key = request.args.get('api_key')

    if api_key is None:
        return missing_parameter('Missing required parameter.')

    if api_key == current_app.config.get('API_ADMIN_KEY') or api_key == current_app.config.get('API_READ_KEY'):
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
                return jsonify(status_code=200, content={'message': 'No matches found'})
        except SQLAlchemyError as error:
            return jsonify(status_code=500, content={'message': 'Error encountered trying to read user table.' + str(error)})
        
    else:
        return unauthorized('Unauthorized access attempt.')