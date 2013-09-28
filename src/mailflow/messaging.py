from kombu import Exchange
from mailflow.front import app

mail_exchange = Exchange(app.config['NEW_MESSAGE_EXCHANGE_NAME'], type='topic', durable=False)


def get_routing_key(*args):
    return ".".join(
        [app.config['NEW_MESSAGE_QUEUE_PREFIX']] + map(str, args)
    )
