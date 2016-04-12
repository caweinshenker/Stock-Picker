#!flask/bin/python

#all the imports
from flask import Flask, g, request, session, redirect, url_for, abort, render_template, flash, send_file
from flask.ext.uploads import UploadSet, configure_uploads
from forms import *
import matplotlib.pyplot as plt, mpld3
import matplotlib.patches as mpatches
import os
import datetime
import numpy
import psycopg2
import StringIO
import psycopg2.extras
import getpass


#configuration
DEBUG = True
UPLOAD_FOLDER = 'uploads/'
txtfiles = UploadSet('text', ('txt',))
app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
configure_uploads(app, (txtfiles,))
app.config.from_object(__name__)
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
	return render_template('stock.html', ticker = ticker) 

@app.route('/index/<ticker>/fig')
def fig(ticker = None):
	conn = init_db()
	cur = connect_db(conn)
	cur.execute("SELECT * FROM stock_price WHERE ticker='" + str(ticker) + "'ORDER BY pdate")
	prices = [dict(ticker = row[0], pdate = row[1], open_price = row[2], close = row[3]) for row in cur.fetchall()]
	dates = []
	opens = []
	closes = []
	for day in prices:
		dates.append(day["pdate"])
		opens.append(day["open_price"])
		closes.append(day["close"])
	close_db(cur, conn)
	mindate = min(dates)
	maxdate = max(dates)
	minopen = min(opens)
	maxopen = max(opens)
	minclose = min(closes)
	maxclose = max(closes)
	plt.rcParams.update({'font.size': 12})
	plt.plot(dates, opens, 'r-', dates, closes, 'b-')
	plt.xlabel('Date')
	plt.ylabel('Price')
	red_patch = mpatches.Patch(color = 'red', label = 'Open price')
	blue_patch = mpatches.Patch(color = 'blue', label = 'Close price')
	plt.legend(handles=[red_patch, blue_patch])
	fig = plt.gcf()
	img = StringIO.StringIO()
	fig.savefig(img)
	img.seek(0)
	plt.close()
	close_db(cur, conn)
	return send_file(img, mimetype='image/png') 

@app.route('/pick', methods=['GET', 'POST'])
def show_picker():	
	form = PickForm()
	if form.validate_on_submit():
		conn= init_db()
		cur = connect_db(conn)
		filename = secure_filename(form.upload.data.filename)
		form.upload.data.save(UPLOAD_FOLDER + filename)
		SQL =  'INSERT INTO text (author_name, file_location, description, title, text_type, pub_date) VALUES (%s %s %s %s %s %s)'
		data = (form.author, filename, form.textType, form.description, form.title, form.textType, str(form.pub_date))
		cur.execute(SQL, data)
		close_db(cur, conn)
		return redirect(url_for('results.html', form = form))		
	else:
		filename = None
	return render_template('pick.html', form=form, filename=filename)
	

def init_db():
	try:
		connectionString = 'dbname = caweinsh_sp3 user=caweinsh password=f6nt0d host=localhost'
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


