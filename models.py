from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Beverage(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    type = db.Column(db.String(150), nullable = False)
    price = db.Column(db.String(30), nullable = False)
    proof = db.Column(db.String(200), nullable = False)
    origin = db.Column(db.String(200), nullable = False)
    vintage = db.Column(db.String(200), nullable = True)
    description = db.Column(db.String(500), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,type,price,proof,origin,user_token,vintage='Blank',description='Blank', id = ''):
        self.id = self.set_id()
        self.name = name
        self.type = type
        self.price = price
        self.proof = proof
        self.origin = origin
        self.vintage = vintage
        self.description = description
        self.user_token = user_token


    def __repr__(self):
        return f'The following beverage has been added to the inventory: {self.nickname}'

    def set_id(self):
        return (secrets.token_urlsafe())

class BeverageSchema(ma.Schema):
    class Meta:
        fields = ['id','name','type','price','proof','origin','vintage','description']

beverage_schema = BeverageSchema()
beverages_schema = BeverageSchema(many=True)