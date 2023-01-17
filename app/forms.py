from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import EqualTo, InputRequired

class SignUpForm (FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name")
    email = EmailField("Email", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()

class AddressForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name')
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    submit = SubmitField()