from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext import restful
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object('mailflow.settings')
db = SQLAlchemy(app)
restful_api = restful.Api(app)

lm = LoginManager()
lm.init_app(app)

CsrfProtect(app)

import views, models, admin, api

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)
restful_api.add_resource(api.MessageList, '/api/message')
restful_api.add_resource(api.Message, '/api/message/<int:message_id>')
restful_api.add_resource(api.InboxList, '/api/inbox')
restful_api.add_resource(api.Inbox, '/api/inbox/<int:inbox_id>')
restful_api.add_resource(api.InboxCleaner, '/api/inbox/<int:inbox_id>/truncate')


def initdb():
    db.create_all()
    user_datastore.create_role(name='admin', description='')
    user = user_datastore.create_user(email='admin@example.com', password='1234')
    db.session.commit()
    admin_role = user_datastore.find_role("admin")
    user_datastore.add_role_to_user(user, admin_role)
    db.session.commit()


def main():
    app.run(debug=True)
