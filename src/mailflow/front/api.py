from flask import request
from flask.ext import restful
from mailflow.front import models, app
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
        return {
            'count': len(inboxes),
            'data': [
                dict(
                    id=inbox.id,
                    name=inbox.name,
                    total_messages=inbox.message_count
                )
                for inbox in inboxes
            ]
        }

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
        inbox = models.Inbox.get(inbox_id)
        if inbox is None:
            return error(404, "Inbox with id={0} not found".format(inbox_id))
        if inbox.user_id != g.user.id:
            return error(403, "You are not allowed to access mailbox with id id={0}".format(inbox_id))

        form = MessageListForm(request.args)
        if not form.validate():
            return error(400, "Invalid request parameters", errors=form.errors)

        page = form.page.data

        if inbox.message_count > 0 and page > inbox.page_count:
            return error(404, 'Page {0} not found'.format(page))

        messages = inbox.messages_page(page)

        return {
            'id': inbox.id,
            'name': inbox.name,
            'login': inbox.login,
            'password': inbox.password,
            'host': app.config['INBOX_HOST'],
            'port': app.config['INBOX_PORT'],
            'messages_on_page': len(messages),
            'total_messages': inbox.message_count,
            'page_number': page,
            'total_pages': inbox.page_count,
            'messages': [
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
        if inbox is None:
            return error(404, 'Inbox with id={0} not found'.format(inbox_id))
        if inbox.user_id != g.user.id:
            return error(403, 'You are not allowed to edit inbox')

        inbox.truncate()
        return None, 200
