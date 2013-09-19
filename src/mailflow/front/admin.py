from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user
from mailflow.front import app, db
from mailflow.front.models import User, Role, Inbox, Message


admin = Admin(app)


class SecuredModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin

admin.add_view(SecuredModelView(User, db.session))
admin.add_view(SecuredModelView(Role, db.session))
admin.add_view(SecuredModelView(Inbox, db.session))
admin.add_view(SecuredModelView(Message, db.session))
