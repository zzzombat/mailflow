import sys
import logging
import hashlib
import pyzmail

from flask.ext.script import Command, Option

from mailflow.front import models

logger = logging.getLogger(__name__)


class Deliver(Command):

    option_list = [
        Option('--user', '-u', dest='user'),
        Option('--recipient', '-r', dest='recipient'),
        Option('--sender', '-s', dest='sender'),
    ]

    def run(self, user, recipient, sender):
        logging.basicConfig(level=logging.INFO, filename='/tmp/debug-deliver.log')

        inbox = models.Inbox.query.filter(models.Inbox.login == user).first()

        logger.info("new message by user '%s' from '%s' to '%s'", user, sender, recipient)
        input = sys.stdin.read()

        try:
            self.parse_message(inbox, sender, recipient, input)
            return 0
        except Exception, e:
            logger.exception('error occured during message parsing')
            print >> sys.stderr, "Internal error"
            return 1

    def parse_message(self, inbox, mail_from, rcpt_to, raw_message):
        parsed_message = pyzmail.PyzMessage.factory(raw_message)
        message = models.Message()
        models.db.session.add(message)

        message.inbox = inbox
        message.from_addr = mail_from
        message.to_addr = rcpt_to
        message.subject = parsed_message.get_subject()
        for part in parsed_message.mailparts:
            if not part.is_body:
                continue
            if part.type == 'text/plain':
                message.body_plain = part.get_payload()
            if part.type == 'text/html':
                message.body_html = part.get_payload()

        message.source = hashlib.sha1(raw_message).hexdigest()
        message.get_source_file().write(raw_message)
        models.db.session.commit()
        return message
