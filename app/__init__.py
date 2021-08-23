import os
from flask import Flask
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import firebase_admin


def create_app(config_class=Config):
    # firebase_cred = firebase_admin.credentials.Certificate(Config.FIREBASE_CRED_PATH)
    # firebase_app = firebase_admin.initialize_app(firebase_cred)
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cojo_applog',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('cojo_app startup')
    return app