from flask import jsonify, request, current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from app.users.models import User, UserSchema
from app.api.users import bp as users_api
from app.users.utils import clear_user_table
from app.api.errors import bp as errors_api


CORS(users_api)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_api.route('/api/users/clear')
def clear_user_data():
    api_key = request.args.get('api_key')

    if api_key is None:
        return errors_api.missing_parameter('Missing required parameter.')
        
    if api_key == current_app.config.get('API_ADMIN_KEY'):
        try:
            clear_user_table()
            return jsonify(status_code=200, content={'message': 'Succesfully cleared user database.'})
        except SQLAlchemyError as error:
            return jsonify(status_code=200, content={'message': 'Error encountered trying to clear user table.' + str(error)})
        
    else:
        return errors_api.unauthorized('Unautorized access attempted.')
    
@users_api.route('/api/users/dump')
def dump_user_table():
    api_key = request.args.get('api_key')

    if api_key is None:
        return errors_api.missing_parameter('Missing required parameter.')
    
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
        return errors_api.unauthorized('Unauthorized access attempt.')
    
@users_api.route('/api/users/<lname>/dump')
def dump_users_by_lname(lname):
    api_key = request.args.get('api_key')

    if api_key is None:
        return errors_api.missing_parameter('Missing required parameter.')

    if api_key == current_app.config.get('API_ADMIN_KEY') or api_key == current_app.config.get('API_READ_KEY'):
        try:
            lname = lname.capitalize()
            users = User.query.filter_by(lname=lname).all()
            results = []
            if users is not None and len(results) > 0:
                for user in users:
                    user.phone = str(user.phone)
                    results.append(user)
                data = users_schema.dump(results)
                return jsonify(status_code=200, result=data), 200
            else:
                return jsonify(status_code=200, content={'message': 'No matches found'}), 200
        except SQLAlchemyError as error:
            return jsonify(status_code=500, content={'message': 'Error encountered trying to read user table.' + str(error)})
        
    else:
        return errors_api.unauthorized('Unauthorized access attempt.')