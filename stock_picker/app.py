#!flask/bin/python

#all the imports
from flask import Flask, g, request, session, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
import matplotlib.pyplot as plt, mpld3
import os
import numpy
import psycopg2
import psycopg2.extras
import getpass

#configuration
app = Flask(__name__)
DEBUG = True
app.config.from_object(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://caweinsh:f6n60d@localhost:5432/caweinsh_sp3'
#db = SQLAlchemy(app)
cur = None
conn = None
PER_PAGE = 30

@app.route('/')
def homepage():
	return render_template('home.html')
	

#@app.route('/stocks', defaults={'page':1})
#@app.route('/stocks/page/<int:page>')
@app.route('/index')
def show_stocks():
	conn = init_db()
	cur = connect_db(conn)
	cur.execute('SELECT ticker, company_name FROM stock ORDER BY ticker;')
	entries = [dict(ticker = row[0], company = row[1]) for row in cur.fetchall()]
	close_db(cur, conn)
	return render_template('index.html', entries=entries)

@app.route('/index/<ticker>')
def show_stock(ticker = None):
	conn = init_db()
	cur = connect_db(conn)
	cur.execute("SELECT * FROM stock_price WHERE ticker='" + str(ticker) + "'ORDER BY pdate")
	prices = [dict(ticker = row[0], pdate = row[1], open_price = row[2], close = row[3]) for row in cur.fetchall()]
	dates = []
	opens = []
	closes = []
	for day in prices:
		dates.append(day[pdate])
		opens.append(day[open_price])
		closes.append(day[close])
	plt.plot(dates, opens, 'r--', dates, closes, 'bs')
	plt.xlabel('date')
	plt.ylabel('prices')
	fig = plt.figure()
	fig_html = mpld3.fig_to_html(fig)
	return render_template('stock.html', dates = dates, opens=opens, closes=closes, prices = prices, fig_html = fig_html) 


@app.route('/pick')
def show_picker():	
	#TODO
	conn= init_db()
	cur = connect_db(conn)


#@app.route('/about')
#def show_about():
#	return render_template('templates/about.html')

#'''


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
		connectionString = 'dbname = caweinsh_sp3 user=caweinsh password=f6nt0d host=localhost'
		print(connectionString)
		conn = psycopg2.connect(connectionString)
	except Exception as e:
		print(str(e))
	return conn

def connect_db(conn):
	return conn.cursor()


def close_db(cur, conn):
	cur.close()
	conn.close()


if __name__=='__main__':
	app.run()
