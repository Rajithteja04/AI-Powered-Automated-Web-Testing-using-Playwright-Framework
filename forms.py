from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('developer', 'Developer'), ('qa', 'QA Engineer'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')

class GenerateForm(FlaskForm):
    browser = SelectField('Browser', choices=[
        ('chromium', 'Chrome/Chromium'),
        ('firefox', 'Firefox'),
        ('webkit', 'Safari/WebKit')
    ], default='chromium', validators=[DataRequired()])
    predefined = SelectField('Predefined Requirements', choices=[
        ('', 'Select a predefined requirement...'),
        ('search', 'Search for a product on Amazon'),
        ('login', 'Login to Amazon account'),
        ('cart', 'Add item to cart'),
        ('checkout', 'Complete checkout process'),
        ('full_flow', 'Complete Amazon Purchase Flow (Login -> Search -> Add to Cart -> Checkout)'),
        ('failed_login', 'Test failed login attempt'),
        ('out_of_stock', 'Test out of stock item handling'),
        ('invalid_payment', 'Test invalid payment method'),
        ('guest_checkout', 'Test guest checkout without account')
    ])
    requirement = TextAreaField('Testing Requirement', validators=[
        DataRequired(),
        Length(min=10, max=1000, message="Requirement must be between 10 and 1000 characters."),
        Regexp(r'^[a-zA-Z0-9\s\.,!?\'"_\-@/:]+$', message="Requirement contains invalid characters.")
    ], render_kw={"rows": 6})
    submit = SubmitField('Generate & Execute Test')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[Length(max=100)])
    submit = SubmitField('Search')

class CodeGenerateForm(FlaskForm):
    browser = SelectField('Browser', choices=[
        ('chromium', 'Chrome/Chromium'),
        ('firefox', 'Firefox'),
        ('webkit', 'Safari/WebKit')
    ], default='chromium', validators=[DataRequired()])
    requirement = TextAreaField('Feature Requirement', validators=[
        DataRequired(),
        Length(min=10, max=1000, message="Requirement must be between 10 and 1000 characters."),
        Regexp(r'^[a-zA-Z0-9\s\.,!?\'"_\-@/:]+$', message="Requirement contains invalid characters.")
    ], render_kw={"rows": 6, "placeholder": "Describe the new feature you want to add to your Flask app..."})
    project_zip = FileField('Project Zip File', validators=[
        FileRequired(),
        FileAllowed(['zip'], 'Only .zip files are allowed!')
    ], description="Upload your Flask project as a .zip file for code analysis")
    submit = SubmitField('Generate Code & Test')
