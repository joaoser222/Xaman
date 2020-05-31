from flask import Flask
from flask_cors import CORS
public_dir = '../frontend/dist/spa'
app = Flask(__name__, instance_relative_config=True,template_folder=public_dir,static_folder=public_dir,static_url_path='/')
from app.config import Config
from flask_login import LoginManager
login = LoginManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)
from app import routes,models