import os
import logging
from flask import Flask, render_template, request
from flask_login import LoginManager
from extensions import limiter, cache
from config import config
from models import db, User

app = Flask(__name__)
config_name = os.environ.get('FLASK_ENV') or 'development'
app.config.from_object(config[config_name])

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Setup rate limiting
limiter.init_app(app)

# Setup caching
cache.init_app(app)

# Setup logging
logging.basicConfig(level=getattr(logging, app.config['LOG_LEVEL']),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f'404 error: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 error: {str(error)}')
    db.session.rollback()
    return render_template('500.html'), 500

# Import and register blueprints
from auth import auth as auth_blueprint
from routes import main as main_blueprint
from admin import admin as admin_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
