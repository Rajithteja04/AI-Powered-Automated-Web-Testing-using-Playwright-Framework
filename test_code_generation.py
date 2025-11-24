#!/usr/bin/env python3
"""
Test script to verify the fixed code generation and integration guide functionality.
This tests the agents directly without running the full Flask application.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.code_generator import generate_code
from agents.integration_guide import generate_integration_guide

# Mock state data for testing
mock_extracted_code = {
    'app.py': """
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
""",
    'routes.py': """
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User
from forms import LoginForm, RegistrationForm
from utils.zip_handler import extract_zip

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        # Handle code generation
        pass
    return render_template('generate.html')

@main.route('/history')
@login_required
def history():
    return render_template('history.html')

@main.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
""",
    'models.py': """
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
""",
    'forms.py': """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
""",
    'config.py': """
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
""",
    'templates': {
        'base.html': '<!DOCTYPE html><html><head><title>{% block title %}Base{% endblock %}</title></head><body>{% block content %}{% endblock %}</body></html>',
        'home.html': '{% extends "base.html" %}{% block content %}<h1>Welcome Home</h1>{% endblock %}',
        'generate.html': '{% extends "base.html" %}{% block content %}<h1>Generate Code</h1><form method="post"><input type="text" name="requirement"><button type="submit">Generate</button></form>{% endblock %}'
    },
    'project_structure': ['app.py', 'routes.py', 'models.py', 'forms.py', 'config.py', 'templates/base.html', 'templates/home.html', 'templates/generate.html']
}

class MockState:
    def __init__(self, requirement, extracted_code, generated_code=None):
        self.requirement = requirement
        self.extracted_code = extracted_code
        self.generated_code = generated_code or {}
        self.framework = 'flask'

def test_code_generation():
    """Test the code generation agent."""
    print("Testing Code Generation...")

    state = MockState(
        requirement="Add a user profile page that shows user information and allows editing",
        extracted_code=mock_extracted_code
    )

    try:
        result = generate_code(state)
        generated_code = result.get('generated_code', {})

        print("Generated Code Keys:", list(generated_code.keys()))

        # Check if it's proper JSON structure
        if isinstance(generated_code, dict):
            print("✓ Generated code is proper JSON structure")

            # Check for expected keys
            expected_keys = ['routes_code', 'template_code', 'css_code', 'js_code', 'models_code', 'forms_code']
            for key in expected_keys:
                if key in generated_code:
                    print(f"✓ Contains {key}")
                    if key == 'routes_code' and generated_code[key]:
                        print(f"  Routes code preview: {generated_code[key][:200]}...")
                    elif key == 'template_code' and generated_code[key]:
                        print(f"  Template files: {list(generated_code[key].keys())}")
                else:
                    print(f"✗ Missing {key}")
        else:
            print("✗ Generated code is not a dictionary")
            print("Output:", generated_code)

    except Exception as e:
        print(f"✗ Error in code generation: {e}")

def test_integration_guide():
    """Test the integration guide agent."""
    print("\nTesting Integration Guide...")

    # First generate some code
    state = MockState(
        requirement="Add a user profile page that shows user information and allows editing",
        extracted_code=mock_extracted_code
    )

    code_result = generate_code(state)
    generated_code = code_result.get('generated_code', {})

    # Now test integration guide
    state.generated_code = generated_code

    try:
        result = generate_integration_guide(state)
        instructions = result.get('integration_instructions', '')

        print("Integration Instructions Length:", len(instructions))

        # Check if it contains project-specific information
        if 'routes.py' in instructions:
            print("✓ Contains routes.py references")
        else:
            print("✗ Missing routes.py references")

        if 'templates/' in instructions:
            print("✓ Contains template references")
        else:
            print("✗ Missing template references")

        if 'Flask' in instructions or 'flask' in instructions:
            print("✓ Contains Flask-specific instructions")
        else:
            print("✗ Missing Flask-specific instructions")

        print("Instructions preview:")
        print(instructions[:500] + "..." if len(instructions) > 500 else instructions)

    except Exception as e:
        print(f"✗ Error in integration guide: {e}")

if __name__ == '__main__':
    test_code_generation()
    test_integration_guide()
