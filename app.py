#!flask/bin/python
#all the imports
from flask import Flask, g, request, session, redirect, url_for, abort, render_template, flash, send_file
from flask.ext.uploads import UploadSet, configure_uploads
from werkzeug import secure_filename
import time
from datetime import datetime
import sys
import os
import datetime
import json
import ast
import collections
import psycopg2
import psycopg2.extras
import getpass
sys.path.insert(0, 'helpers/')
from parser import Parser
from forms  import UploadForm, PickForm, StockForm, SearchForm
from pagination import Pagination
from database import Db
from nyt_parser import NYT_Parser


#configuration
app = Flask(__name__)
app.config['UPLOADED_TEXT_DEST'] = 'uploads/'
DEBUG = True
txtfiles = UploadSet('text', ('txt',))
app.secret_key = 'secret'
reload(sys)
sys.setdefaultencoding('utf8')
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
	price_SQL = "SELECT open_price, close_price, high, low, pdate FROM stock_prices WHERE ticker = %s ORDER BY pdate;"
	volume_SQL = "SELECT volume, vdate FROM stock_volumes where ticker = %s ORDER BY vdate;"
	dividend_SQL = "SELECT price, ddate from stock_dividends where ticker = %s ORDER BY ddate;"
	price_dates = []
	open_prices = []
	high_prices = []
	low_prices  = []
	close_prices = []
	volumes = []
	dividends = []	
	db.execute(price_SQL, data)	
	for row in db.fetchall():
		date_js = int(time.mktime(row[4].timetuple())) * 1000
		open_prices.append([date_js, float(row[0])])
		high_prices.append([date_js, float(row[2])])
		low_prices.append([date_js,  float(row[3])])
		close_prices.append([date_js, float(row[1])])
	db.execute(volume_SQL, data)
	for row in db.fetchall():
		date_js = int(time.mktime(row[1].timetuple())) * 1000
		volumes.append([date_js, float(row[0])])
	db.execute(dividend_SQL, data)
	for row in db.fetchall():
		date_js = int(time.mktime(row[1].timetuple())) * 1000
		dividends.append([date_js, float(row[0])])
	if form.validate_on_submit():
		date = str(form.date_field.data).split()[0]
		nyt = NYT_Parser()
		nyt.find_articles(company, date)
		articles = nyt.get_news()
		return render_template('stock.html', form = form, open_prices = open_prices,close_prices = close_prices, volumes = volumes, dividends = dividends, company = company, ticker = ticker, validated = True, articles = articles) 
	else:
		return render_template('stock.html', form = form, open_prices = open_prices,close_prices = close_prices, volumes = volumes, dividends = dividends, company = company, ticker = ticker) 



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
		parser = Parser(textfile, investment, start_date, end_date)
		start_value = parser.start_value
		end_value = parser.end_value
		portfolio = parser.portfolio_growth
		net_change = end_value - start_value
		stocks = parser.portfolio
		growth = collections.OrderedDict(sorted(parser.portfolio_growth.items()))
		growth_array = []
		for key, value in growth.items():
			date_js = int(time.mktime(key.timetuple())) * 1000
			growth_array.append([date_js, float("{0:.2f}".format(value))])
		return render_template('text_result.html',textname = textname, portfolio = portfolio, stocks = stocks, start_date = start_date, end_date = end_date, investment = investment, net_change = net_change, start_value = start_value, end_value = end_value, growth_array=growth_array)
	else:
		return render_template('pick.html', form = form)   	
	

@app.route('/about')
def about():
	#TODO
	return render_template('about.html')

@app.route('/pick/<textname>')
def show_text_result(textname = None, textfile = None, start_date = None, end_date = None, investment = None):
	parser = Parser(textfile, investment, start_date, end_date)
	return render_template('templates/text_result.html', textname = textname, parser = parser)

	
if __name__=='__main__':
	app.run()

