SQLALCHEMY_DATABASE_URI = "postgres://@/mailflow"
SECRET_KEY = 'Chi6riup1gaetiengaShoh=Wey1pohph0ieDaes7eeph'

RAW_EMAIL_FOLDER = "/var/tmp"

RABBITMQ_URI = 'amqp://mailflow:youneverguess@localhost//mail'
RABBITMQ_EXCHANGE_NAME = 'mail'
RABBITMQ_MAIL_QUEUE_PREFIX = 'newmail'
