import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Blueprint

app = Flask(__name__)
# Read configuration to apply from environment
config_name = os.environ.get('FLASK_CONFIG', 'development')
# apply configuration
cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
app.config.from_pyfile(cfg)

# initialize extensions
db = SQLAlchemy()
db.init_app(app)

# Create a blueprint
api = Blueprint('api', __name__)
# Import the endpoints belonging to this blueprint
from . import endpoints
from . import errors


@api.before_request
def before_request():
    """All routes in this blueprint require authentication."""
    if app.config['AUTH_REQUIRED']:
        token_header = app.config['TOKEN_HEADER']
        if request.headers.get(token_header):
            token = request.headers[token_header]
            if token == app.config['SECRET_TOKEN']:
                app.logger.info('Validated request token')
            else:
                app.logger.warn('Unauthorized: Invalid request token')
                return jsonify({'error': 'Invalid request token'}), 401
        else:
            app.logger.error('Unauthorized: No request token included')
            return jsonify({'error': 'unauthorized'}), 401


# register blueprints
app.register_blueprint(api, url_prefix=app.config['URL_PREFIX'])
