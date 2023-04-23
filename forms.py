from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField
from wtforms.validators import InputRequired,Length

class UserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Email',validators=[InputRequired(),Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(),Length(max=30)])
    last_name = StringField('First Name', validators=[InputRequired(),Length(max=30)])

class UserFormLogin(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired()])

class FeedBackForm(FlaskForm):
    title = StringField('Title')
    content = StringField('Content')
    
