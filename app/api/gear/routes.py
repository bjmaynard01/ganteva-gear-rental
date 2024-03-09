from flask import jsonify, request, current_app
from app.gear.models import GearCategories, GearCategoriesSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from app.api.gear import bp as gear_api
from app.api.errors import bp as errors_api

gear_schema = GearCategoriesSchema()
gears_schema = GearCategoriesSchema(many=True)

@gear_api.route('/api/gear/categories/dump')
def dump_gear_categories():
    api_key = request.args.get('api_key')

    if api_key is None:
        return errors_api.missing_parameter('Missing required parameter.')
    
    if api_key == current_app.config.get('API_ADMIN_KEY') or api_key == current_app.config.get('API_READ_KEY'):
        try:
            gear_cats = GearCategories.query.all()
            results = []
            for gear_cat in gear_cats:
                results.append(gear_cat)
            data = gears_schema.dump(results)
            return jsonify(status_code=200, result=data)
        except SQLAlchemyError as error:
            return jsonify(status_code=200, content={'message': 'Error encountered trying to read user table.' + str(error)})
        
    else:
        return errors_api.unauthorized('Unauthorized access attempt.')
