from flask.ext.assets import Bundle

js_lib = Bundle(
    'js/lib/jquery.min.js',
    'js/lib/bootstrap.min.js',
    'js/lib/angular.min.js',
    'js/lib/angular-route.min.js',
    'js/lib/angular-sanitize.min.js',
    'js/lib/angular-resource.js',
    filters='jsmin',
    output='compiled/lib.js'
)


js = Bundle(
    'js/app.js',
    'js/controllers/inbox_list.js',
    'js/controllers/inbox.js',
    'js/controllers/message.js',
    'js/services.js',
    'js/filters.js',
    'js/routes.js',
    filters='jsmin',
    output='compiled/main.js'
)
