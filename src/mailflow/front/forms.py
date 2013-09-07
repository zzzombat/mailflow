# -*- coding: utf-8 -*-
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

        if user is None or user.password != form.password.data:
            message = "Неверный email или пароль".decode('utf-8')
            raise ValidationError(message)

        if not user.active:
            message = "Учетная запись не активна".decode('utf-8')
            raise ValidationError(message)


class RegistrationForm(Form):
    email = TextField(validators=[Required()])
    password = PasswordField(validators=[Required()])

    def validate_email(form, field):
        if db.session.query(models.User).filter_by(email=field.data).count() > 0:
            message = "Пользователь с таким адресом уже существует".decode('utf-8')
            raise ValidationError(message)


