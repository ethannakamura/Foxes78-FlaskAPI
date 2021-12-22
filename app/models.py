# import sqlalchemy to create our instance of our ORM (translator between python and SQL)
from flask_sqlalchemy import SQLAlchemy

# import our LoginManager and instantiate
from flask_login import LoginManager, UserMixin

# imports for tools for our models
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from uuid import uuid4

# actually create the instance of SQLAlchemy
db = SQLAlchemy()

# instance of login manager
login = LoginManager()

# necessary user_loader function that flask_login needs us to write in order to work
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# let's set up our User object
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=True, default='')
    last_name = db.Column(db.String(100), nullable=True, default='')
    password = db.Column(db.String(150), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, username, email, password, first_name='', last_name=''):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password) # salt and hash this password
        self.id = str(uuid4()) # generate an id in some manner


# design a new object - player object - that will be the focus of my API CRUD operations
# also looking toward the future I'm probably planning to use this model for my ecommerce website
class Player(db.Model):
    id = db.Column(db.String, primary_key=True)
    number = db.Column(db.Integer)
    first_name = db.Column(db.String(150), nullable=False) # first_name VARCHAR(150) not null
    last_name = db.Column(db.String(150), nullable=True) # last_name VARCHAR(150)
    position = db.Column(db.String(15))
    team = db.Column(db.String(150), nullable=False, default='Free Transfer')
    nationality = db.Column(db.String(150))
    transfer_cost = db.Column(db.String(150), nullable=False, default='$0m')

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'postion': self.position,
            'team': self.team,
            'nationality': self.nationality,
            'transfer_cost': self.transfer_cost
            }