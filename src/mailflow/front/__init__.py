from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
import flask.ext.restless
import mailflow.front.api_utils

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object('mailflow.settings')
db = SQLAlchemy(app)

import views, models, admin

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(models.Inbox, methods=['GET', 'POST', 'DELETE'])
manager.create_api(models.Message, methods=['GET', 'DELETE'],
                   preprocessors={
                       'GET_MANY':[api_utils.pre_get_many_message],
                   },
                   postprocessors={
                       'GET_MANY':[api_utils.post_get_many_message],
                   })

def main():
    app.run(debug = True)
