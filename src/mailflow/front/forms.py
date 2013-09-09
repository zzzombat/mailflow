# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms.validators import Required, ValidationError, NumberRange
from wtforms import fields, Form as BaseForm

from mailflow.front import db, models


class LoginForm(Form):
    email = fields.TextField('email', validators=[Required()])
    password = fields.PasswordField('password', validators=[Required()])
    remember_me = fields.BooleanField('remember_me', default=False)

    def validate_email(self, field):
        user = db.session.query(models.User).filter_by(email=field.data).first()

        if user is None or user.password != self.password.data:
            message = "Неверный email или пароль".decode('utf-8')
            raise ValidationError(message)

        if not user.active:
            message = "Учетная запись не активна".decode('utf-8')
            raise ValidationError(message)


class RegistrationForm(Form):
    email = fields.TextField(validators=[Required()])
    password = fields.PasswordField(validators=[Required()])

    def validate_email(self, field):
        if db.session.query(models.User).filter_by(email=field.data).count() > 0:
            message = "Пользователь с таким адресом уже существует".decode('utf-8')
            raise ValidationError(message)


class MessageListForm(BaseForm):
    inbox_id = fields.IntegerField(validators=[Required(), NumberRange(min=1)])
    page = fields.IntegerField(validators=[NumberRange(min=1)], default=1)
