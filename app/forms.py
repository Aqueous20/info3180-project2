from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, DataRequired
from wtforms.fields import EmailField, DecimalField
from datetime import datetime


class RegisterForm(FlaskForm):
  name = StringField('name', validators=[InputRequired()])
  username = StringField('Username', validators=[InputRequired()])
  email = EmailField('Email Address', validators=[DataRequired()])
  biography = TextAreaField('Biography', validators=[DataRequired()])
  location = StringField('Location', validators=[InputRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  date_joined = datetime.now()
  photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg','png'], 'Images Only!')])


class CarForm(FlaskForm):
  description = TextAreaField('Description', validators=[DataRequired()])
  make = StringField('Make', validators=[InputRequired()])
  model = StringField('Model', validators=[InputRequired()])
  colour = StringField('Colour', validators=[InputRequired()])
  year = StringField('Year', validators=[InputRequired()])
  transmission = SelectField('Transmission', validators=[InputRequired()])
  car_type = SelectField('Car Type', validators=[InputRequired()])
  price = DecimalField('Price', validators=[InputRequired()])
  photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg','png'], 'Images Only!')])

class SearchForm(FlaskForm):
  make = StringField('Make', [DataRequired()])
  model = StringField('Model', [DataRequired()])
  
  
class LoginForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[DataRequired()])