from kombu import Connection, Exchange
from mailflow import settings

mail_exchange = Exchange(settings.RABBITMQ_EXCHANGE_NAME, 'topic', durable=True)


def new_email(email_id, user_id):
    with Connection(settings.RABBITMQ_URI) as conn:
        with conn.Producer(serializer='json') as producer:
            producer.publish(
                {'email_id': email_id, 'user_id': user_id},
                exchange=mail_exchange,
                roting_key=get_queue_name('{0}.#'.format(user_id)),
                declare=[mail_exchange]
            )


def get_queue_name(name):
    return "{0}.{1}".format(settings.RABBITMQ_MAIL_QUEUE_PREFIX, name)
