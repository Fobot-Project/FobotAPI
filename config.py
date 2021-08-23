import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env_path = '/fobot.env'
load_dotenv(dotenv_path=basedir+env_path)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # FIREBASE_CRED_PATH = os.path.join(basedir,'credentials',os.environ.get('FIREBASE_PATH'))
    HASH_SECRET_SALT = os.environ.get('HASH_SECRET_SALT')
    PORT = os.environ.get('PORT')