from werkzeug.contrib.profiler import ProfilerMiddleware
from flask.ext.script import Server
from mailflow.front import app


class Profile(Server):

    def handle(self, *args, **kwargs):
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        super(Profile, self).handle(*args, **kwargs)
