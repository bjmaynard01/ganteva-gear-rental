from flask import render_template, request, jsonify
from app import db
from app.errors import bp as errors_bp

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify(status_code=404, message="Resource not found"), 404
    else:
        return render_template('errors/404.html', title='Page Not Found'), 404
    

@errors_bp.app_errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api'):
        db.session.rollback()
        return jsonify(status_code=500, message='Internal server error'), 500
    else:
        db.session.rollback()
        return render_template('errors/500.html', title='Internal Server Error'), 500
    
@errors_bp.app_errorhandler(401)
def unauthorized_for_access():
    if request.path.startswith('/api/'):
        return jsonify(status_code=401, message="Unauthorized access attempted."), 401
    else:
        return render_template('errors/401.html', title='Unauthorized'), 401