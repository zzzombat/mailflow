from flask.ext.wtf import Form
from wtforms.validators import Required, ValidationError
from wtforms import TextField, BooleanField, PasswordField

from mailflow.front import db, models

class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    def validate_email(form, field):
        user = db.session.query(models.User).filter_by(email=field.data).first()

        if user is None:
            raise ValidationError('Invalid email')

        if user.password != form.password.data:
            raise ValidationError('Invalid password')



class RegistrationForm(Form):
    email = TextField(validators=[Required()])
    password = PasswordField(validators=[Required()])

    def validate_email(form, field):
        if db.session.query(models.User).filter_by(email=field.data).count() > 0:
            raise ValidationError('Duplicate email')

