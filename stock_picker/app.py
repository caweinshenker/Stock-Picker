#!flask/bin/python
#all the imports
from flask import Flask, g, request, session, redirect, url_for, abort, render_template, flash, send_file
from flask.ext.uploads import UploadSet, configure_uploads
from math import ceil
from werkzeug import secure_filename
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
from parser import Parser
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
	db = Db()
	SQL = "SELECT ticker, company_name FROM stocks WHERE ticker LIKE %s OR company_name LIKE %s ORDER BY ticker;"
	data =  ('%', '%')	
	if search.validate_on_submit():
		search_data = search.search.data
		data = (search_data + '%', search_data + '%')
		db.execute(SQL, data)
		entries = [dict(ticker = row[0], company = row[1]) for row in db.fetchall()]
		return render_template('index.html', search = SearchForm(),  entries = entries)

	else:
		db.execute(SQL, data)
		entries = [dict(ticker = row[0], company = row[1]) for row in db.fetchall()]
		return render_template('index.html',search = search, entries=entries)


@app.route('/index/stock/<ticker>', methods = ['GET', 'POST'])
def show_stock(ticker = None):
	form = StockForm()
	db = Db()
	SQL = "SELECT company_name FROM stocks where ticker = %s;"
	data = (ticker,)
	db.execute(SQL, data)
	company = db.fetchall()[0][0]
	if form.validate_on_submit():
		date = str(form.date_field.data).split()[0]	
		data = (ticker, date)
		SQL = "SELECT open_price, close_price, high, low FROM stock_prices WHERE ticker = %s AND pdate = %s;"
		db.execute(SQL, data)
		results = db.fetchall()
		if len(results) < 1:
			return render_template('stock.html', date = date, company = company, no_results = True, form = StockForm(), ticker = ticker)
		else:
			tup = results[0]
			return render_template('stock.html', no_results = False, company = company, date = str(form.date_field.data).split()[0], validated = True, form = StockForm(), ticker = ticker, open_price = tup[0], close_price = tup[1], high = tup[2], low = tup[3])
	else:
		return render_template('stock.html', form = form, company = company, ticker = ticker) 


@app.route('/index/<ticker>/fig')
def fig(ticker = None):
	db = Db()
	SQL = ("SELECT * FROM stock_prices WHERE ticker=%s ORDER BY pdate;")
	data = (ticker,)
	db.execute(SQL, data)
	open_close = Open_Close_Graph(ticker, db.fetchall())
	open_close.make_graph()
	img = open_close.get_fig()
	return send_file(img, mimetype='image/png') 

@app.route('/upload', methods=['GET', 'POST'])
def upload():	
	form = UploadForm()
	if form.validate_on_submit():
		flash('TXT registered')
		db = Db()
		filename = secure_filename(form.upload.data.filename)
		form.upload.data.save(os.path.join(app.config['UPLOADED_TEXT_DEST'], filename))
		SQL =  'INSERT INTO text (author_name, file_location, description, title, text_type, pub_date) VALUES (%s, %s, %s, %s, %s, %s);'
		data = (form.author.data, "uploads/" + form.upload.data.filename, form.description.data, form.title.data, form.textType.data, form.pub_date.data)
		db.execute(SQL, data)
		return redirect(url_for('pick'))

	else:
		filename = None
	return render_template('upload.html', form=form, filename=filename)


@app.route('/pick', methods = ['GET', 'POST'])
def pick():
	form = PickForm()
	if form.validate_on_submit():
		textname = form.text.data.split("/")[1].split(".")[0]
		textfile  = form.text.data
		start_date = str(form.start_date.data).split()[0]
		end_date = str(form.end_date.data).split()[0]
		investment = form.money.data
		#print(textname)
		#print(textfile)
		#print(start_date)
		#print(end_date)
		#return redirect(url_for('show_text_result', textname=textname, textfile = textfile, start_date = start_date, end_date = end_date, investment = investment,))
		parser = Parser(textfile, investment, start_date, end_date)
		return render_template('text_result.html', parser = parser)
	else:
		print("Nope")
		return render_template('pick.html', form = form)   	
	
@app.route('/about')
def about():
	#TODO
	return render_template('about.html')

@app.route('/pick/<textname>')
def show_text_result(textname = None, textfile = None, start_date = None, end_date = None, investment = None):
	parser = Parser(textfile, investment, start_date, end_date)	
	return render_template('templates/text_result.html', parser = parser)

	
if __name__=='__main__':
	app.run()

