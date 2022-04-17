# import os

class Config:
    SECRET_KEY = "\xf5\xf7\x99\x9f8\xce\xecc\xf8a\x0b\xac\x97\xd1\x05\xfd" # os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///web.db" #os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'projectflask513@gmail.com' #os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD =  "nzlvnkoqkfbeyxjv" #os.environ.get('EMAIL_PASSWORD')

