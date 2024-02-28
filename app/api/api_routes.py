from app import app, models
from flask import jsonify

@app.route('/api/hello')
def hello():
    return jsonify(status=200, message='Hello, World!'), 200