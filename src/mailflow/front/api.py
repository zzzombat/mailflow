from flask import request
from flask.ext import restful
from mailflow.front import models
from sqlalchemy.exc import IntegrityError


class MessageList(restful.Resource):
    def get(self):
        inbox_id = int(request.args.get('inbox_id', 0))
        messages = models.Message.query
        if inbox_id:
            messages = messages.filter_by(inbox_id=inbox_id)
        result = {
            'count': len(messages.all()),
            'data': [dict(id=m.id, from_addr=m.from_addr, to_addr=m.to_addr, subject=m.subject) for m in messages.all()]
        }
        return result


class Message(restful.Resource):
    def get(self, message_id):
        message = models.Message.query.get(message_id)
        if not message:
            return None, 404
        return {'id': message.id,
                'from_addr': message.from_addr,
                'to_addr': message.from_addr,
                'subject': message.to_addr,
                'body_plain': message.body_plain,
                'body_html': message.body_html,
                }

    def delete(self, message_id):
        message = models.Message.query.get(message_id)
        if not message:
            return None, 404
        models.db.session.delete(message)
        models.db.session.commit()
        return '', 204


class InboxList(restful.Resource):
    def get(self):
        inboxes = models.Inbox.query
        result = {
            'count': len(inboxes.all()),
            'data': [dict(id=i.id, name=i.name) for i in inboxes.all()]
        }
        return result

    def post(self):
        try:
            inbox = models.Inbox(**request.json)
        except Exception:
            return '', 400
        models.db.session.add(inbox)
        try:
            models.db.session.commit()
        except IntegrityError as exc:
            return repr(exc), 400
        return '', 201


class Inbox(restful.Resource):
    def get(self, inbox_id):
        inbox = models.Inbox.query.get(inbox_id)
        if not inbox:
            return None, 404
        return {'id': inbox.id,
                'name': inbox.name,
                'login': inbox.login,
                'password': inbox.password}

    def delete(self, inbox_id):
        inbox = models.Inbox.query.get(inbox_id)
        if not inbox:
            return None, 404
        models.db.session.delete(inbox)
        models.db.session.commit()
        return '', 204


class InboxCleaner(restful.Resource):
    def post(self, inbox_id):
        inbox = models.Inbox.query.get(inbox_id)
        if not inbox:
            return None, 404
        models.Message.query.filter_by(inbox_id=inbox_id).delete()
        models.db.session.commit()
        return '', 200
