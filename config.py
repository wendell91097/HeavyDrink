import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    """
        SET CONFIG VARIABLES FOR THE FLASK APP
        USING ENVIRONMENT VARIABLES WHERE AVAILABLE
        OTHERWISE CREATE THE CONFIG VARIABLE IF NOT DONE ALREADY
    """

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('MY_KEY_IS_OBVIOUS') or "wendiesel"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_NOTIFICATIONS = False