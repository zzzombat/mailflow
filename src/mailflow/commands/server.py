from gevent.wsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from werkzeug.contrib.profiler import ProfilerMiddleware
from flask.ext.script import Command, Option


class GeventServer(Command):

    description = 'Runs the Flask development server with gevent'

    def __init__(self, host='127.0.0.1', port=5000, use_debugger=True,
                 use_reloader=True, profile=False, profile_max=30,
                 **options):

        self.port = port
        self.host = host
        self.use_debugger = use_debugger
        self.use_reloader = use_reloader
        self.profile = profile
        self.profile_max = profile_max
        self.server_options = options

    def get_options(self):
        return (
            Option('-t', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('--profile',
                   action='store_true',
                   dest='profile',
                   default=self.profile),

            Option('--profile-max',
                   type=int,
                   dest='profile_max',
                   default=self.profile_max),
        )

    def handle(self, app, host, port, profile, profile_max):
        """Runs a development server."""
        if profile:
            wsgi = ProfilerMiddleware(app, restrictions=[profile_max])
        elif self.use_debugger:
            wsgi = DebuggedApplication(app)
        else:
            wsgi = app

        def run():
            print('Start server at: {0}:{1}'.format(host, port))

            http_server = WSGIServer((host, port), wsgi, **self.server_options)
            http_server.serve_forever()

        if self.use_reloader:
            run = run_with_reloader(run)

        run()
