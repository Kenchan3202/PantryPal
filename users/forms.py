from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email


class RegisterForm(FlaskForm):
    # Date of Birth field
    dob_regexp = Regexp(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$',
                        message="Invalid date format, must be DD/MM/YYYY")
    dob = StringField('Date of Birth', validators=[DataRequired(), dob_regexp])

    email = EmailField('Email', validators=[DataRequired(), Email(
        message="Invalid email address")])

    # Firstname and Lastname: Exclude specified characters
    name_regexp = Regexp(r'^[^*?!\'^+%&/()=}]{3,}$',
                         message="Invalid characters in name")
    first_name = StringField('Firstname',
                             validators=[DataRequired(), name_regexp])
    last_name = StringField('Lastname', validators=[DataRequired(), name_regexp])

    # Password: Specific length and character requirements
    password_regexp = Regexp(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,12}$',
                             message="Password must be 6-12 characters long, include digits, lowercase, uppercase, and special characters")
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=12),
                                         password_regexp])

    # Confirm Password: Must match Password
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message="Passwords must match")])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username (Email)', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# from flask_wtf import FlaskForm
# from wtforms import PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, EqualTo
#
#
# class ChangePasswordForm(FlaskForm):
#     current_password = PasswordField('Current Password', validators=[DataRequired()])
#     new_password = PasswordField('New Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
#     show_password = BooleanField('Show Password')
#     submit = SubmitField('Change Password')

# import re
# from flask_wtf import FlaskForm, RecaptchaField
# from wtforms import StringField, SubmitField, PasswordField, BooleanField
# from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
#
#
# def character_check(form, field):
#     excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
#
#     for char in field.data:
#         if char in excluded_chars:
#             raise ValidationError(f"Character {char} is not allowed.")
#
#
# def phone_validation(form, field):
#
#     phone_pattern = re.compile(r'^\d{4}-\d{3}-\d{4}$')
#
#     if not phone_pattern.match(field.data):
#         raise ValidationError('Phone number must be in the format: XXXX-XXX-XXXX')
#
#
# def password_validation(form, field):
#     password = field.data
#
#     password_pattern = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])')
#
#     if not password_pattern.match(password):
#         raise ValidationError('Password must contain at least 1 digit, 1 lowercase character, 1 uppercase letter and '
#                               '1 special characters.')
#
#
# def date_of_birth_validation(form, field):
#     date_of_birth = field.data
#
#     date_of_birth_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')
#
#     if not date_of_birth_pattern.match(date_of_birth):
#         raise ValidationError('Date of birth must be in the format: DD/MM/YYYY - D(DAY), M(Month), Y(Year)')
#
#
# # def postcode_validation(form, field):
# #     postcode = field.data
# #
# #     postcode_pattern = re.compile(r'^[A-Z]\d{2}\s?[A-Z]{0,2}\d[A-Z]{2}$')
# #
# #     if not postcode_pattern.match(postcode):
# #         raise ValidationError('Postcode must be in the format: XY XXX, XYY YXX, or XXY YXX')
#
#
#
# class RegisterForm(FlaskForm):
#     email = StringField(validators=[DataRequired(), Email()])
#     first_name = StringField(validators=[DataRequired(), character_check])  # 修改为 first_name
#     last_name = StringField(validators=[DataRequired(), character_check])  # 修改为 last_name
#     dob = StringField(validators=[DataRequired(), date_of_birth_validation])
#     # postcode = StringField(validators=[DataRequired(), postcode_validation])
#     # phone = StringField(validators=[DataRequired(), phone_validation])
#     password = PasswordField(validators=[Length(min=6, max=12)])
#     confirm_password = PasswordField(validators=[EqualTo('password', message='Passwords must match!'), password_validation])
#     submit = SubmitField()
#
# class LoginForm(FlaskForm):
#     email = StringField(validators=[DataRequired(), Email()])
#     password = PasswordField(validators=[DataRequired()])
#     postcode = StringField(validators=[DataRequired()])
#     pin = StringField(validators=[DataRequired()])
#     recaptcha = RecaptchaField()
#     submit = SubmitField()
#
# class PasswordForm(FlaskForm):
#     current_password = PasswordField(id='password', validators=[DataRequired()])
#     show_password = BooleanField('Show password', id='check')
#     new_password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message="Must be between 6 and 12 characters in length"), password_validation])
#     confirm_new_password = PasswordField(validators=[DataRequired(), EqualTo('new_password', message='Both new password fields must be equal')])
#     submit = SubmitField('Change Password')
#
# import re
# from flask_wtf import FlaskForm, RecaptchaField
# from wtforms import StringField, SubmitField, PasswordField, BooleanField
# from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
#
#
# def character_check(form, field):
#     excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
#
#     for char in field.data:
#         if char in excluded_chars:
#             raise ValidationError(f"Character {char} is not allowed.")
#
#
# def phone_validation(form, field):
#
#     phone_pattern = re.compile(r'^\d{4}-\d{3}-\d{4}$')
#
#     if not phone_pattern.match(field.data):
#         raise ValidationError('Phone number must be in the format: XXXX-XXX-XXXX')
#
#
# def password_validation(form, field):
#     password = field.data
#
#     password_pattern = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])')
#
#     if not password_pattern.match(password):
#         raise ValidationError('Password must contain at least 1 digit, 1 lowercase character, 1 uppercase letter and '
#                               '1 special characters.')
#
#
# def date_of_birth_validation(form, field):
#     date_of_birth = field.data
#
#     date_of_birth_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')
#
#     if not date_of_birth_pattern.match(date_of_birth):
#         raise ValidationError('Date of birth must be in the format: DD/MM/YYYY - D(DAY), M(Month), Y(Year)')
#
#
# # def postcode_validation(form, field):
# #     postcode = field.data
# #
# #     postcode_pattern = re.compile(r'^[A-Z]\d{2}\s?[A-Z]{0,2}\d[A-Z]{2}$')
# #
# #     if not postcode_pattern.match(postcode):
# #         raise ValidationError('Postcode must be in the format: XY XXX, XYY YXX, or XXY YXX')
#
#
#
# class RegisterForm(FlaskForm):
#     email = StringField(validators=[DataRequired(), Email()])
#     first_name = StringField(validators=[DataRequired(), character_check])
#     last_name = StringField(validators=[DataRequired(), character_check])
#     dob = StringField(validators=[DataRequired(), date_of_birth_validation])
#     # postcode = StringField(validators=[DataRequired(), postcode_validation])
#     # phone = StringField(validators=[DataRequired(), phone_validation])
#     password = PasswordField(validators=[Length(min=6, max=12)])
#     confirm_password = PasswordField(validators=[EqualTo('password', message='Passwords must match!'), password_validation])
#     submit = SubmitField()
#
# class LoginForm(FlaskForm):
#     email = StringField(validators=[DataRequired(), Email()])
#     password = PasswordField(validators=[DataRequired()])
#     postcode = StringField(validators=[DataRequired()])
#     pin = StringField(validators=[DataRequired()])
#     recaptcha = RecaptchaField()
#     submit = SubmitField()
#
# class PasswordForm(FlaskForm):
#     current_password = PasswordField(id='password', validators=[DataRequired()])
#     show_password = BooleanField('Show password', id='check')
#     new_password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message="Must be between 6 and 12 characters in length"), password_validation])
#     confirm_new_password = PasswordField(validators=[DataRequired(), EqualTo('new_password', message='Both new password fields must be equal')])
#     submit = SubmitField('Change Password')
