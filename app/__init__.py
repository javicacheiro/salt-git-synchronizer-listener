import os
from flask import Flask
from flask import Blueprint

app = Flask(__name__)
# Read configuration to apply from environment
config_name = os.environ.get('FLASK_CONFIG', 'development')
# apply configuration
cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
app.config.from_pyfile(cfg)

# Create a blueprint
api = Blueprint('api', __name__)
# Import the endpoints belonging to this blueprint
from . import endpoints
from . import errors


@api.before_request
def before_request():
    """All routes in this blueprint require authentication."""
    if app.config['AUTH_REQUIRED']:
        if request.args.get('secret_token'):
            token = request.args.get('secret_token')
            if token == app.config['SECRET_TOKEN']:
                app.logger.info('Validated request token')
            app.logger.warn('Unauthorized: Invalid request token')
        app.logger.warn('Unauthorized: No request token included')
        return jsonify({'error': 'unauthorized'}), 401
    app.logger.info('No authentication required')


# register blueprints
app.register_blueprint(api, url_prefix=app.config['URL_PREFIX'])
