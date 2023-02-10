class Config(object):
    pass

class ProdConfig(object):
    pass

class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SECRET_KEY = '\x81\xde\x99\xd6\xe3e\x10(\xce\xfc\xbb\xb9'