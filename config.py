import os

class config:
    SECRET_KEY = os.environ.get('MAILER_PROJECT_SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    USER_ATTACHMENTS = 'E:\\Mailer\\static\\attachments'
    ALLOWED_EXTENSIONS = ['PDF', 'XLSX']
    ATTACHMENT_PHOTOS = 'static/images/'

class prod_config(config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class dev_config(config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


