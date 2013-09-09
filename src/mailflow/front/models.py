import datetime
import string
from random import sample

from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship

from mailflow.front import db
from mailflow import storage
from mailflow import settings


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


def _get_date():
    return datetime.datetime.now()


def _generate_string(count):
    sample_string = sample(string.letters + string.digits, count)
    return ''.join(sample_string)


class GeneralMixin:
    creation_date = db.Column(db.DateTime(), default=_get_date)
    modification_date = db.Column(db.DateTime(), onupdate=_get_date)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)

        return d


class Role(db.Model, RoleMixin, GeneralMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin, GeneralMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)


class Inbox(db.Model, GeneralMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    login = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255), index=True)
    user = relationship("User")

    def __init__(self, name=None):
        self.name = name
        super(Inbox, self).__init__()

    def generate_credentials(self):
        if not self.login:
            self.login = _generate_string(settings.INBOX_LOGIN_LENGTH)

        if not self.password:
            self.password = _generate_string(settings.INBOX_PASSWORD_LENGTH)


def generate_credentials_listener(mapper, connect, target):
    target.generate_credentials()
listen(Inbox, 'before_insert', generate_credentials_listener)


class Message(db.Model, GeneralMixin):
    id = db.Column(db.Integer, primary_key=True)
    inbox_id = db.Column(db.Integer, db.ForeignKey('inbox.id'))
    from_addr = db.Column(db.String(255))
    to_addr = db.Column(db.String(255))
    subject = db.Column(db.Text())
    body_plain = db.Column(db.Text())
    body_html = db.Column(db.Text())
    source = db.Column(db.Text())
    inbox = relationship("Inbox", cascade="all")

    @classmethod
    def get_page_for_inbox_id(cls, inbox_id, page=1):
        limit = page * settings.INBOX_PAGE_SIZE
        offset = (page - 1) * settings.INBOX_PAGE_SIZE

        return cls.query \
                  .filter_by(inbox_id=inbox_id) \
                  .order_by(cls.creation_date.desc()) \
                  .slice(offset, limit) \
                  .all()

    @classmethod
    def count_for_inbox_id(cls, inbox_id):
        return cls.query.filter_by(inbox_id=inbox_id).count()

    def get_source_file(self, mode='ab+'):
        return storage.fs.open(self.source, mode)
