import re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Email, ValidationError, DataRequired, length, EqualTo, Length


class AddItemForm(FlaskForm):
    newItem = StringField(validators=[DataRequired()])
    itemQuantity = IntegerField(validators=[DataRequired()])
    itemUnits = StringField(validators=[DataRequired()])
    listName = StringField(validators=[DataRequired()])
    submit = SubmitField()
