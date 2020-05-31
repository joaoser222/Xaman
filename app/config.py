import os
from dotenv import load_dotenv
from pathlib import Path 

env_path = '../.env'
load_dotenv(dotenv_path=env_path)
class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY','you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI','sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)