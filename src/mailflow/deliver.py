
"""

Simple.

"""

import sys
import logging
import hashlib
import argparse
import pyzmail
from mailflow.front import models

logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('user')
    parser.add_argument('recipient')
    parser.add_argument('sender')
    return parser.parse_args()

def parse_message(inbox_id, mail_from, rcpt_to, raw_message):
    parsed_message = pyzmail.PyzMessage.factory(raw_message)
    message = models.Message()
    models.db.session.add(message)

    message.inbox_id = inbox_id
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

def main():
    logging.basicConfig(level=logging.INFO, filename='/tmp/debug-deliver.log')
    args = get_args()
    
    inbox = models.Inbox.query.filter(models.Inbox.login==args.user).first()
    if not inbox:
        logger.error('cannot find inbox with login %s', args.user)
        print >> sys.stderr, "Cannot find inbox with login %s" % args.user
        return 1

    logger.info("new message by user '%s' from '%s' to '%s'", args.user, args.sender, args.recipient)
    try:
        message = parse_message(inbox.id, args.sender, args.recipient, sys.stdin.read())
        return 0
    except Exception, e:
        logger.exception('error occured during message parsing')
        print >> sys.stderr, "Internal error"
        return 1
