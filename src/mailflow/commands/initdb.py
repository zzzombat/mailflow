from flask.ext.script import Command

from mailflow.front import db, models


class InitDB(Command):

    def run(self):
        db.create_all()
        db.session.commit()
        admin = models.User(
            email='admin@example.com',
            password='1234',
            active=True,
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()
