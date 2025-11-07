import os

class Config:
    SECRET_KEY = os.environ["FLASKBLOG_SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ["FLASKBLOG_GMAIL"]
    MAIL_PASSWORD = os.environ["FLASKBLOG_PASSWORD"]
    MAIL_DEFAULT_SENDER = os.environ["FLASKBLOG_GMAIL"]
    DEBUG = True