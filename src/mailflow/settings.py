# General app configuration
SQLALCHEMY_DATABASE_URI = "postgres://mailflow.user:1234@localhost/mailflow"
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = 5 * 3600
SQLALCHEMY_MAX_OVERFLOW = 20

LOG_LEVEL = 'INFO'
LOG_FILE = 'webapp.log'

SECRET_KEY = 'Chi6riup1gaetiengaShoh=Wey1pohph0ieDaes7eeph'

STORAGE_CLASS = 'fs.contrib.davfs.DAVFS'
STORAGE_ARGS = {
    'url': 'http://localhost/media',
    'credentials': {
        'username': 'admin',
        'password': '$up3r$3cr3t'
    }
}

INBOX_LOGIN_LENGTH = 16
INBOX_PASSWORD_LENGTH = 16
INBOX_PAGE_SIZE = 50

INBOX_HOST = 'mailflow.openpz.org'
INBOX_PORT = 25

WTF_CSRF_TIME_LIMIT = 21600

CACHE_TYPE = 'memcached'
CACHE_DEFAULT_TIMEOUT = 300

CACHE_MEMCACHED_SERVERS = ('localhost:11211', )

# Celery configuration
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_IMPORTS = ("mailflow.tasks", )
CELERY_TASK_SERIALIZER = 'json'

NEW_MESSAGE_QUEUE_PREFIX = "newmail"
NEW_MESSAGE_EXCHANGE_NAME = "newmail"
NEW_MESSAGE_QUEUE_POSTFIX_LENGTH = 10
