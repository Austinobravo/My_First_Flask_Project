from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file   import FileField,FileAllowed


#Post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
   # date = DateTimeField("Date")
    image_upload= FileField("Post Picture", validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post')
