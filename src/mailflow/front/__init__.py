from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object('mailflow.settings')
db = SQLAlchemy(app)

import views, models, admin

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

def main():
    app.run(debug = True)
