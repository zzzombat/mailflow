from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object('mailflow.settings')
db = SQLAlchemy(app)
import views, models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_role(name='admin', description='')
    user = user_datastore.create_user(email='admin@example.com', password='1234')
    db.session.commit()
    admin_role = user_datastore.find_role("admin")
    user_datastore.add_role_to_user(user, admin_role)
    db.session.commit()

def main():
    app.run(debug = True)
