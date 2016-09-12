import os

DEBUG = True
AUTH_REQUIRED = False
URL_PREFIX = '/git/v1'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data.sqlite')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + db_path
SQLALCHEMY_TRACK_MODIFICATIONS = False
