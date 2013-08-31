from flask import Flask
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required

app = Flask(__name__, static_folder='static', static_url_path='/static')
admin = Admin(app, name='Mailflow')
app.config.from_object('mailflow.settings')
db = SQLAlchemy(app)

import views, models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

def main():
    app.run(debug = True)
