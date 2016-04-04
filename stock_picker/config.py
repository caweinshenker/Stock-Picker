import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = ""
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']	


class Production Config(Config):
	DEBUG = False

class StagingConfig(Config):
	DEVELOPMENT = TRUE
	DEBUG = TRUE

class TestingConfig(Config):
	TESTING = True

	
