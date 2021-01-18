import os

class config:
    SECRET_KEY = os.environ.get('MAILER_PROJECT_SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    USER_ATTACHMENTS = 'E:\\Mailer\\static\\attachments'
    ALLOWED_EXTENSIONS = ['PDF', 'XLSX']
    ATTACHMENT_PHOTOS = 'static/images/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    APP_MAIL = "mailerservices365@gmail.com"
    APP_MAIL_PASSWORD = "MailerService77"
    APP_PORT = 465
    ADMIN_TWILIO_NUMBER = "+17023303417"
    TWILIO_AUTH_TOKEN = "a04aa23e43e35f035f87f1fd75e72442"
    TWILIO_ACCOUNT_SID = "ACf80e16b608a2bd89c61c31dedd924af1"
    ADMIN_CONTACT = "+201065630331"

class prod_config(config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class dev_config(config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


