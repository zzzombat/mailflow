import os

import logging
from logging.handlers import WatchedFileHandler

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext import restful
from flask.ext.login import LoginManager
from flask.ext.cache import Cache
from flask_wtf.csrf import CsrfProtect

# Use gevent if activated
# Optionally, set up psycopg2 & SQLAlchemy to be greenlet-friendly.
# Note: psycogreen does not really monkey patch psycopg2 in the
# manner that gevent monkey patches socket.
#
if "PSYCOGREEN" in os.environ:

    # Do our monkey patching
    #
    from gevent.monkey import patch_all
    patch_all()
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()

    using_gevent = True
else:
    using_gevent = False

# App initialization
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Load default settings
app.config.from_object('mailflow.settings')
# Load production and development settings
app.config.from_pyfile('../local_settings.py', silent=True)
app.config.from_envvar('MAILFLOW_CONFIG', silent=True)

# Configure logging
if not app.debug:
    handler = WatchedFileHandler(app.config['LOG_FILE'])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
else:
    # Development server will intercept logging automatically
    # so no need for StreamHandler
    handler = logging.NullHandler()
    handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

# Configure database
db = SQLAlchemy(app)
if using_gevent:
    # Assuming that gevent monkey patched the builtin
    # threading library, we're likely good to use
    # SQLAlchemy's QueuePool, which is the default
    # pool class.  However, we need to make it use
    # threadlocal connections
    db.engine.pool._use_threadlocal = True

restful_api = restful.Api(app)

lm = LoginManager()
lm.init_app(app)

CsrfProtect(app)

cache = Cache(app)

import views, models, admin, api

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)
restful_api.add_resource(api.Message, '/api/message/<int:message_id>')
restful_api.add_resource(api.InboxList, '/api/inbox')
restful_api.add_resource(api.Inbox, '/api/inbox/<int:inbox_id>')
restful_api.add_resource(api.InboxCleaner, '/api/inbox/<int:inbox_id>/truncate')


def main():
    app.run(debug=True)
