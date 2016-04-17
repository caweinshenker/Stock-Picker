#!flask/bin/python
#all the imports
from flask import Flask, g, request, session, redirect, url_for, abort, render_template, flash, send_file
from flask.ext.uploads import UploadSet, configure_uploads
from math import ceil
import sys
import os
import datetime
import numpy
import psycopg2
import StringIO
import psycopg2.extras
import getpass
sys.path.insert(0, 'helpers/')
from graphs import Open_Close_Graph
from forms  import PickForm, SearchForm
from helpers import buy_stocks_from_portfolio.py as stockBuyer
from helpers import parse_text_for_portfolio.py as textParser
from helpers import construct_trie_from_tickers.py as trieMaker
from forms  import UploadForm, PickForm, StockForm, SearchForm
from pagination import Pagination
from database import Db

#configuration
app = Flask(__name__)
app.config['UPLOADED_TEXT_DEST'] = 'uploads/'
DEBUG = True
txtfiles = UploadSet('text', ('txt',))
app.secret_key = 'secret'
configure_uploads(app, (txtfiles,))
PER_PAGE = 30
app.config.from_object(__name__)

@app.route('/')
def homepage():
	return render_template('home.html')
	

#@app.route('/stocks', defaults={'page':1})
#@app.route('/stocks/page/<int:page>')
@app.route('/index/<searchterm>', methods = ['GET', 'POST'])
@app.route('/index')
def show_stocks(searchterm = '', page = None):
	search = SearchForm()
	conn = init_db()
	cur = connect_db(conn)
	SQL = "SELECT ticker, company_name FROM stocks WHERE ticker LIKE %s OR company_name LIKE %s ORDER BY ticker;"
	data =  ('%', '%')	
	if search.validate_on_submit():
		search_data = search.search.data
		data = (search_data + '%', search_data + '%')
		cur.execute(SQL, data)
		entries = [dict(ticker = row[0], company = row[1]) for row in cur.fetchall()]
		close_db(cur,conn)
		return render_template('index.html', search = SearchForm(),  entries = entries)

	else:
		cur.execute(SQL, data)
		entries = [dict(ticker = row[0], company = row[1]) for row in cur.fetchall()]
		close_db(cur, conn)
		return render_template('index.html',search = search, entries=entries)


@app.route('/index/stock/<ticker>', methods = ['GET', 'POST'])
def show_stock(ticker = None):
	form = StockForm()
	conn = init_db()
	cur  = connect_db(conn)
	if form.validate_on_submit():
		date = str(form.date_field.data).split()[0]	
		data = (ticker, date)
		SQL = "SELECT open_price, close_price, high, low FROM stock_prices WHERE ticker = %s AND pdate = %s"
		cur.execute(SQL, data)
		results = cur.fetchall()
		if len(results) < 1:
			close_db(cur, conn)
			return render_template('stock.html', date = date, no_results = True, form = StockForm(), ticker = ticker)
		else:
			tup = results[0]
			close_db(cur, conn)
			return render_template('stock.html', no_results = False, date = str(form.date_field.data), validated = True, form = StockForm(), ticker = ticker, open_price = tup[0], close_price = tup[1], high = tup[2], low = tup[3])
	else:
		return render_template('stock.html', form = form, ticker = ticker) 


@app.route('/pick/<filename>/results')
def show_results(ticker = None, filename= None, form = None):
	#TODO
	return render_template('results.html', filename = filename, form = form)

@app.route('/index/<ticker>/fig')
def fig(ticker = None):
	conn = init_db()
	cur = connect_db(conn)
	cur.execute("SELECT * FROM stock_prices WHERE ticker='" + str(ticker) + "'ORDER BY pdate")
	open_close = Open_Close_Graph(ticker, cur)
	open_close.make_graph()
	img = open_close.get_fig()
	close_db(cur, conn)
	return send_file(img, mimetype='image/png') 

@app.route('/upload', methods=['GET', 'POST'])
def upload():	
	form = UploadForm()
	if form.validate_on_submit():
		flash('TXT registered')
		conn= init_db()
		cur = connect_db(conn)
		filename = secure_filename(form.upload.data.filename)
		form.upload.data.save(os.path.join(app.config['UPLOADED_TEXT_DEST'], filename))
		SQL =  'INSERT INTO text (author_name, file_location, description, title, text_type, pub_date) VALUES (%s, %s, %s, %s, %s, %s)'
		data = (form.author.data, "uploads/" + form.upload.data.filename, form.description.data, form.title.data, form.textType.data, form.pub_date.data)
		cur.execute(SQL, data)
		conn.commit()
		close_db(cur, conn)
		return redirect(url_for('homepage', ticker = ticker, filename = filename, form = form))
	else:
		filename = None
	return render_template('upload.html', form=form, filename=filename)


@app.route('/pick', methods = ['GET', 'POST'])
def pick():
	form = PickForm()
	if form.validate_on_submit():
		flash('Pick complete')
		return redirect(url_for('show_results')) 
	return render_template('pick.html', form = form)   	

	
@app.route('/about')
def about():
	#TODO
	return render_template('about.html')

@app.route('/text_result')
def show_text_result():
	#TODO
	
	return render_template('templates/text_result.html')
	

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
	conn.commit()
	cur.close()
	conn.close()


if __name__=='__main__':
	app.run()


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


