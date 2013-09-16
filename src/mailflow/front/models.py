import datetime
import string
import math
from random import sample

from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy import select, func
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship, column_property

from mailflow.front import db, cache
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


class GeneralMixin(object):
    creation_date = db.Column(db.DateTime(), default=_get_date)
    modification_date = db.Column(db.DateTime(), onupdate=_get_date)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

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


class Message(db.Model, GeneralMixin):
    id = db.Column(db.Integer, primary_key=True)
    inbox_id = db.Column(db.Integer, db.ForeignKey('inbox.id', ondelete='CASCADE'))
    from_addr = db.Column(db.String(255))
    to_addr = db.Column(db.String(255))
    subject = db.Column(db.Text())
    body_plain = db.Column(db.Text())
    body_html = db.Column(db.Text())
    source = db.Column(db.Text())
    inbox = relationship("Inbox", backref='messages', cascade="all")

    def get_source_file(self, mode='ab+'):
        return storage.fs.open(self.source, mode)


def invalidate_message_cache(mapper, connect, target):
    invalidate_inbox_cache(mapper, connect, target.inbox)
listen(Message, 'after_insert', invalidate_message_cache)
listen(Message, 'after_delete', invalidate_message_cache)


class Inbox(db.Model, GeneralMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    login = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255), index=True)
    user = relationship("User")

    message_count = column_property(
        select([func.count(Message.id)]).where(Message.inbox_id == id).correlate_except(Message)
    )

    @classmethod
    @cache.memoize(3600)
    def get(cls, pk):
        return cls.query.get(pk)

    @classmethod
    @cache.memoize(3600)
    def get_for_user_id(cls, user_id):
        return cls.query \
            .filter_by(user_id=user_id) \
            .order_by(cls.id) \
            .all()

    def __init__(self, name=None):
        self.name = name
        super(Inbox, self).__init__()

    @cache.memoize(3600)
    def messages_page(self, page):
        limit = page * settings.INBOX_PAGE_SIZE
        offset = (page - 1) * settings.INBOX_PAGE_SIZE

        return db.session.query(Message) \
            .filter(Message.inbox == self) \
            .order_by(Message.creation_date.desc()) \
            .slice(offset, limit) \
            .all()

    @property
    def page_count(self):
        return int(math.ceil(float(self.message_count) / float(settings.INBOX_PAGE_SIZE)))

    def truncate(self):
        db.session.query(Message) \
            .filter(Message.inbox_id == self.id) \
            .delete()
        invalidate_inbox_cache(None, None, self)
        db.session.commit()

    def generate_credentials(self):
        if not self.login:
            self.login = _generate_string(settings.INBOX_LOGIN_LENGTH)

        if not self.password:
            self.password = _generate_string(settings.INBOX_PASSWORD_LENGTH)


def invalidate_inbox_cache(mapper, connect, target):
    for page in xrange(1, target.page_count + 1):
        cache.delete_memoized(target.messages_page, target, page)
    cache.delete_memoized(Inbox.get_for_user_id, Inbox, target.user_id)
    cache.delete_memoized(Inbox.get, Inbox, target.id)
    listen(Inbox, 'after_insert', invalidate_inbox_cache)
listen(Inbox, 'after_update', invalidate_inbox_cache)
listen(Inbox, 'after_delete', invalidate_inbox_cache)


def generate_credentials_listener(mapper, connect, target):
    target.generate_credentials()
listen(Inbox, 'before_insert', generate_credentials_listener)
