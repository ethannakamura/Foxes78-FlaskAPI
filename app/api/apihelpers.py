from functools import wraps
from flask import request, jsonify
from app.models import User


def token_required(a_function):
    @wraps(a_function)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('x-access-token') # get the API token provided by the user or get None
        # if there is no token - stop and tell them
        if not token:
            return jsonify({'Access denied':'No API token provided - please register to use CUD routes'})
        # if not valid - stop them and tell them
        u = User.query.filter_by(apitoken=token).first()
        if not u:
            return jsonify({'Access denied': 'Invalid API token - please register to use CUD routes'})
        # if yes valid - let them continue
        return a_function(*args, **kwargs)
    return decorated_function