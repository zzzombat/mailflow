import sys
import hashlib
import pyzmail

from flask.ext.script import Command, Option

from mailflow.front import app
from mailflow.storage import fs
from mailflow.tasks import save_email


class Deliver(Command):

    option_list = [
        Option('--user', '-u', dest='user'),
        Option('--recipient', '-r', dest='recipient'),
        Option('--sender', '-s', dest='sender'),
    ]

    def run(self, user, recipient, sender):
        app.logger.info("new message by user '%s' from '%s' to '%s'", user, sender, recipient)
        input = sys.stdin.read()
        filename = hashlib.sha1(input).hexdigest() + '.eml'
        fs.setcontents(filename, input)

        save_email.delay(user, sender, recipient, filename)
