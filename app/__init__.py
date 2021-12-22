from flask import Flask
from config import Config

# import our blueprints
from .api.routes import api
from .auth.routes import auth

# imports for our database stuff
from .models import db, login
from flask_migrate import Migrate

# create/instantiate our flask object (create our flask app)
app = Flask(__name__)
# and then configure our flask app based on the Config class
app.config.from_object(Config)

# register our blueprint - create that link of communication
app.register_blueprint(api)
app.register_blueprint(auth)

# set up our ORM and Migrate connections
db.init_app(app)
migrate = Migrate(app, db)

# config for our login manager
login.init_app(app)
login.login_view = 'auth.signin'
login.login_message = 'Please sign in to see this page.'
login.login_message_category = 'danger'

# give this app/flask object access to it's routes
from . import routes

# give the app/flask object access to it's database models
from . import models