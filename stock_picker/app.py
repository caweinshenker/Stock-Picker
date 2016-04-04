#!flask/bin/python

#all the imports
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

#configuration
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db_conn = 'postgresql+psycopg2://caweinsh:f6nt0d@localhost/caweinsh_stock_picker'
#DEBUG = True
#USERNAME = 'admin'
#app.config['SQLALCHEMY_DATABASE_URI'] = db_conn
#app.config.from_object(__name__)

from models import Result


@app.route('/')
def hello():
	return "Hellow World!"

if __name__=='__main__':
	app.run()
