SQLALCHEMY_DATABASE_URI = "postgres://@/mailflow"
SECRET_KEY = 'Chi6riup1gaetiengaShoh=Wey1pohph0ieDaes7eeph'

INBOX_LOGIN_LENGTH = 16
INBOX_PASSWORD_LENGTH = 16
INBOX_PAGE_SIZE = 50

INBOX_HOST = 'mailflow.openpz.org'
INBOX_PORT = 25

RAW_EMAIL_FOLDER = "/var/tmp"

RABBITMQ_URI = 'amqp://mailflow:youneverguess@localhost//mail'
RABBITMQ_EXCHANGE_NAME = 'mail'
RABBITMQ_MAIL_QUEUE_PREFIX = 'newmail'
