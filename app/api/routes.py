from flask import Blueprint

# actually set up our blueprint and enable communication between our blueprint and the main flask app
# computers are dumb - if we don't tell the blueprint to exist, it won't exist
# and if we don't tell the application how to talk to the blueprint, it will have no idea how to talk to the blueprint
# instantiate a blueprint
api = Blueprint('api', __name__, url_prefix='/api')


# the decorator for a route belonging to a blueprint starts with @<blueprint_name> instead of @app
@api.route('/')
def test():
    return {'datadatadata': 'ooh look at this fancy data'}
