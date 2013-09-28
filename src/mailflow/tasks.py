import pyzmail

from kombu import Connection
from mailflow.storage import fs
from mailflow.front import celery, models, app

from messaging import mail_exchange, get_routing_key


@celery.task
def save_email(inbox_login, mail_from, rcpt_to, raw_message_file):
    raw_message = fs.getcontents(raw_message_file)

    inbox = models.Inbox.query. \
        filter(models.Inbox.login == inbox_login) \
        .first()

    parsed_message = pyzmail.PyzMessage.factory(raw_message)
    message = models.Message(
        from_addr=mail_from,
        to_addr=rcpt_to,
        subject=parsed_message.get_subject(),
        source=raw_message_file
    )

    message.inbox = inbox
    for part in parsed_message.mailparts:
        if not part.is_body:
            continue
        if part.type == 'text/plain':
            message.body_plain = part.get_payload()
        if part.type == 'text/html':
            message.body_html = part.get_payload()

    models.db.session.add(message)
    models.db.session.commit()

    with Connection(app.config['CELERY_BROKER_URL']) as conn:
        with conn.Producer(serializer='json', exchange=mail_exchange) as producer:
            producer.publish(
                message.to_dict(with_inbox_id=True),
                routing_key=get_routing_key(inbox.user_id, message.id),
            )
