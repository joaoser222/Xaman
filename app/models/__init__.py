from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import hashlib
from app import login
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            
            return fields

        return json.JSONEncoder.default(self, obj)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(254), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    @hybrid_property
    def token(self):
        return hashlib.md5(self.email.encode('utf-8')).hexdigest()
    def __repr__(self):
        return '<User {}>'.format(self.username)  
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), index=True, unique=True)
    engine = db.Column(db.String(50))
    database = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    host = db.Column(db.String(254))
    path = db.Column(db.String(1000))
    type = db.Column(db.String(10))

    def __repr__(self):
        return '<Dataset {}>'.format(self.name)    