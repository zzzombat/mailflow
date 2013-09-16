from flask.ext.script import Manager, Server, Shell

from mailflow.front import app, models, db
from mailflow.commands import InitDB, Deliver

manager = Manager(app)

manager.add_command('runserver', Server(debug=True))
manager.add_command('shell', Shell(make_context=lambda: dict(app=app, db=db, models=models)))
manager.add_command('initdb', InitDB())
manager.add_command('deliver', Deliver())

if __name__ == "__main__":
    manager.run()
