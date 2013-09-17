from flask.ext.script import Command

from mailflow.front import db, user_datastore


class InitDB(Command):

    def run(self):
        db.create_all()
        user_datastore.create_role(name='admin', description='')
        user = user_datastore.create_user(email='admin@example.com', password='1234')
        db.session.commit()
        admin_role = user_datastore.find_role("admin")
        user_datastore.add_role_to_user(user, admin_role)
        db.session.commit()
