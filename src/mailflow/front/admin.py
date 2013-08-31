from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from mailflow.front import app, db
from mailflow.front.models import User, Role, Inbox, Message


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Inbox, db.session))
admin.add_view(ModelView(Message, db.session))