from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    mobileNumber = StringField(label='Mobile Number: ', validators=[Length(max=13), DataRequired()])
    consumerKey = StringField(label='Consumer Key: ', validators=[DataRequired()])
    consumerSecret = StringField(label='Consumer Secret: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    mpin = PasswordField(label='MPIN: ', validators=[Length(min=6, max=6), DataRequired()])
    submit = SubmitField(label='Login')
