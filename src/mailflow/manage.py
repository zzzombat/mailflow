from flask.ext.script import Manager, Server

from mailflow.front import app
from mailflow.commands import initdb, deliver

manager = Manager(app)

manager.add_command('runserver', Server())
manager.add_command('initdb', initdb.InitDB())
manager.add_command('deliver', deliver.Deliver())

if __name__ == "__main__":
    manager.run()
