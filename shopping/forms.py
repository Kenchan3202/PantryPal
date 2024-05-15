import re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField
from wtforms.validators import Email, ValidationError, DataRequired, length, EqualTo, Length


class AddItemForm(FlaskForm):
    newItem = StringField(validators=[DataRequired()])
    submit = SubmitField()
