import math

from flask import request
from flask.ext import restful
from mailflow import settings
from mailflow.front import models
from sqlalchemy.exc import IntegrityError
from flask import g
from functools import wraps

from forms import MessageListForm, InboxForm


def api_login_required(funk):
    @wraps(funk)
    def wrap(*args, **kwargs):
        if g.user.is_anonymous():
            return error(401, "Anonyous users are not allowed to access the dashboard")
        return funk(*args, **kwargs)
    return wrap


def error(code, message, **kwargs):
    return dict(status=code, message=message, **kwargs), code


class MessageList(restful.Resource):
    @api_login_required
    def get(self):
        form = MessageListForm(request.args)
        if not form.validate():
            return error(400, "Invalid request parameters", errors=form.errors)

        inbox_id = form.inbox_id.data
        page = form.page.data

        inbox = models.Inbox.query.get(inbox_id)

        if inbox is None:
            return error(404, "Inbox with id={0} not found".format(inbox_id))

        if inbox.user_id != g.user.id:
            return error(403, "You are not allowed to access mailbox with id id={0}".format(inbox_id))

        total_items = models.Message.count_for_inbox_id(inbox_id)

        if 0 < total_items <= (page - 1) * settings.INBOX_PAGE_SIZE:
            return error(404, 'Page {0} not found'.format(page))

        messages = models.Message.get_page_for_inbox_id(inbox_id, page)

        return {
            'count': len(messages),
            'total_items': total_items,
            'page_number': page,
            'total_pages': math.ceil(float(total_items) / float(settings.INBOX_PAGE_SIZE)),
            'data': [
                dict(
                    id=m.id,
                    from_addr=m.from_addr,
                    to_addr=m.to_addr,
                    subject=m.subject,
                    creation_date=m.creation_date.strftime('%s%f')[:-3]
                )
                for m in messages
            ]
        }


class Message(restful.Resource):
    @api_login_required
    def get(self, message_id):
        message = models.Message.query.get(message_id)
        if not message:
            return error(404, "Message with id={0} not found".format(message_id))

        return {
            'id': message.id,
            'from_addr': message.from_addr,
            'to_addr': message.to_addr,
            'subject': message.subject,
            'body_plain': message.body_plain,
            'body_html': message.body_html,
        }

    @api_login_required
    def delete(self, message_id):
        message = models.Message.query.get(message_id)
        if not message:
            return error(404, "Message with id={0} not found".format(message_id))
        models.db.session.delete(message)
        models.db.session.commit()
        return None, 204


class InboxList(restful.Resource):
    @api_login_required
    def get(self):
        inboxes = models.Inbox.get_for_user_id(g.user.id)
        result = {
            'count': len(inboxes),
            'data': [dict(id=i.id, name=i.name) for i in inboxes]
        }
        return result

    @api_login_required
    def post(self):
        try:
            inbox = models.Inbox(**request.json)
        except Exception:
            return None, 400
        inbox.user_id = g.user.id
        models.db.session.add(inbox)
        try:
            models.db.session.commit()
        except IntegrityError as exc:
            return repr(exc), 400
        return None, 201


class Inbox(restful.Resource):
    @api_login_required
    def get(self, inbox_id):
        inbox = models.Inbox.query.get(inbox_id)
        if inbox is None:
            return error(404, 'Inbox with id={0} not found'.format(inbox_id))
        if inbox.user_id != g.user.id:
            return None, 403
        return {
            'id': inbox.id,
            'name': inbox.name,
            'login': inbox.login,
            'password': inbox.password,
            'host': settings.INBOX_HOST,
            'port': settings.INBOX_PORT
        }

    @api_login_required
    def put(self, inbox_id):
        inbox = models.Inbox.query.get(inbox_id)
        if inbox is None:
            return error(404, 'Inbox with id={0} not found'.format(inbox_id))
        if inbox.user_id != g.user.id:
            return error(403, 'You are not allowed to edit inbox')

        form = InboxForm.from_json(request.json)
        if not form.validate():
            return error(400, 'Invalid form data', errors=form.errors)

        inbox.name = form.name.data
        models.db.session.commit()

        return None, 200

    @api_login_required
    def delete(self, inbox_id):
        inbox = models.Inbox.query.get(inbox_id)
        if not inbox:
            return None, 404
        if inbox.user_id != g.user.id:
            return None, 403
        models.db.session.delete(inbox)
        models.db.session.commit()
        return None, 204


class InboxCleaner(restful.Resource):
    @api_login_required
    def post(self, inbox_id):
        inbox = models.Inbox.query.get(inbox_id)
        if not inbox:
            return None, 404
        if inbox.user_id != g.user.id:
            return None, 403
        models.Message.query.filter_by(inbox_id=inbox_id).delete()
        models.db.session.commit()
        return None, 200
