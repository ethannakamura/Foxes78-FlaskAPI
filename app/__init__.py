from flask import Flask
from config import Config

# import our blueprints
from .api.routes import api
from .auth.routes import auth

# create/instantiate our flask object (create our flask app)
app = Flask(__name__)
# and then configure our flask app based on the Config class
app.config.from_object(Config)

# register our blueprint - create that link of communication
app.register_blueprint(api)
app.register_blueprint(auth)

# give this app/flask object access to it's routes
from . import routes