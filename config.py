# import the os module so that we can read the .env file and access our file system
import os

# give the flask a bit of information about it's own file structure
basedir = os.path.abspath(os.path.dirname(__name__))

# setting up our configuration variables - aka any variables/values that are needed to set up our app
# which we don't want to be public information - for now that's pretty straightforward
# later it'll include things such as our database access keys, payment system integration
class Config:
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=False