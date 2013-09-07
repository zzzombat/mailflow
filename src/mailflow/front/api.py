from flask import request
from flask.ext import restful
from mailflow.front import models
from sqlalchemy.exc import IntegrityError
from flask import g
from functools import wraps


def api_login_required(funk):
    @wraps(funk)
    def wrap(*args, **kwargs):
        if g.user.is_anonymous():
            return None, 401
        return funk(*args, **kwargs)
    return wrap


class MessageList(restful.Resource):
    @api_login_required
    def get(self):
        inbox_id = int(request.args.get('inbox_id', 0))
        if not inbox_id:
            return {
                'status': 400,
                'message': "Parameter inbox_id is required"
            }, 400

        inbox = models.Inbox.query.get(inbox_id)

        if inbox is None:
            return {
                'status': 404,
                'message': "Inbox with id={0} not found".format(inbox_id),
            }, 404

        if inbox.user_id != g.user.id:
            return {
                'status': 403,
                'message': "You are not allowed to access mailbox with id id={0}".format(inbox_id),
            }, 403

        messages = models.Message.query \
                                 .filter_by(inbox_id=inbox_id) \
                                 .order_by(models.Message.creation_date.desc())

        data = [
            dict(
                id=m.id,
                from_addr=m.from_addr,
                to_addr=m.to_addr,
                subject=m.subject,
                creation_date=m.creation_date.strftime('%s%f')[:-3]
            )
            for m in messages.all()
        ]
        return {
            'count': len(messages.all()),
            'data': data
        }


class Message(restful.Resource):
    @api_login_required
    def get(self, message_id):
        message = models.Message.query.get(message_id)
        if not message:
            return None, 404
        return {'id': message.id,
                'from_addr': message.from_addr,
                'to_addr': message.from_addr,
                'subject': message.subject,
                'body_plain': message.body_plain,
                'body_html': message.body_html,
                }

    @api_login_required
    def delete(self, message_id):
        message = models.Message.query.get(message_id)
        if not message:
            return None, 404
        models.db.session.delete(message)
        models.db.session.commit()
        return None, 204


class InboxList(restful.Resource):
    @api_login_required
    def get(self):
        inboxes = models.Inbox.query.filter_by(user_id=g.user.id)
        result = {
            'count': len(inboxes.all()),
            'data': [dict(id=i.id, name=i.name) for i in inboxes.all()]
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
        if not inbox:
            return None, 404
        if inbox.user_id != g.user.id:
            return None, 403
        return {'id': inbox.id,
                'name': inbox.name,
                'login': inbox.login,
                'password': inbox.password}

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
