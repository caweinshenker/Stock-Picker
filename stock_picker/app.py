#!flask/bin/python

#all the imports
from flask import Flask, g, request, session, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
import os
import psycopg2
import getpass

#configuration
app = Flask(__name__)
app.config.from_object(__name__)
conn = None
cur = None
DEBUG = True


@app.route('/')
def homepage():
	return render_template('home.html')
	

@app.route('/index')
def show_stocks():
	init_db()
	connect_db()
	cur = g.db_conn.execute('SELECT ticker, company_name FROM stock order by ticker;')
	entries = [dict(ticker = row[0], company = row[1]) for row in cur.fetchall()]
	close_db()
	return render_template('templates/stock_index.html', entries=entries)


@app.route('/pick')
def show_picker():
	pass


@app.route('about')
def show_about():
	return render_template('templates/about.html)

#@app.teardown_appcontext
#def shutdown_session(exception=None):
#	if cur != None:
#		cur.close()
#	if (conn != None):
#		conn.commit()
#		conn.close()		

#@app.before_request
#def before_request():
#	init_db()
#	connect_db(conn)

#@app.teardown_request
#def teardown_request(exception):
#	if cur != None:
#		cur.close()
#	if (conn != None):
#		conn.commit()
#		conn.close()

def init_db():
	try:
		conn = psycopg2.connect(database = "caweinsh_stock_picker", user = "caweinsh", password = 'f6nt0d')
	except StandardError as e: 
		print(str(e))
		sys.exit(0)
	

def connect_db():
	cur = conn.cursor()

def close_db():
	cur.close()
	conn.close()


if __name__=='__main__':
	app.run()
