import os
import sys

# If we're runing the server we need to monkey patch on app initializion
if 'runserver' in sys.argv:
    os.environ['PSYCOGREEN'] = 'true'

from flask.ext.script import Manager, Shell, Server

from mailflow.front import app, models, db
from mailflow.commands import InitDB, Deliver, GeventServer

manager = Manager(app)

manager.add_command('runserver', GeventServer())
manager.add_command('runblocking', Server())
manager.add_command('shell', Shell(make_context=lambda: dict(app=app, db=db, models=models)))
manager.add_command('initdb', InitDB())
manager.add_command('deliver', Deliver())

if __name__ == "__main__":
    manager.run()
