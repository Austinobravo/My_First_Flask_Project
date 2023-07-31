from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file   import FileField,FileAllowed

from app.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2,max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2,max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Pasword", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    # def validate_email(self, email):
    #     unique_email = User.query.filter_by(email=email.data)
    #     if unique_email:
    #         raise ValidationError('Email already exists') 
        

#Login
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')

#Update form
class UpdateForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2,max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2,max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    image_upload= FileField("Profile Picture", validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

#Request Reset Form
class RequestResetForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('Submit Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Account Not Found.')

# New Password
class NewPassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Pasword", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

