<<<<<<< HEAD
TASKS IN DESCENDING ORDER OF IMPORTANCE -- WITH DEADLINES 
========================================================

1. Get Dividends
	
	DELIVERABLES:
		1. A dividend_seed.py script to load all the dividend data over the past 30 years for the stocks in the database (Using Quandl API)
		2. A CSV of all the dividends for the stocks in the database

	DOCS:
		1.https://www.quandl.com/tools/python
		2.https://www.quandl.com/docs/api#metadata
		3.https://www.quandl.com/blog/getting-started-with-the-quandl-api

	DEADLINE: 4/8/2016


2. Add thread locking/rollback functionality to the current price_seed.py file

	DELIVERABLES:
		An updated price_seed.py file with all the current functionality retained
		
	PROBLEMS:
		40 years of stock data comes out to roughly 100,000,000 million records in the stock_price relation. This takes a
 	        long time, even with 24 threads running. The db machines seem to have a timeout feature that kills any thread that
		runs for too long. If the thread dies this way while the db connection is still open, no more changes to the database
		can be made until all the changes have been rolled back. But you cannot roll back the database until the postgres connectin closes.
		Unfortunately, postgres threads are special special and cannot be killed w/o sudo privileges we do not have on department machines.
		So basically this error causes you to lose your whole damn database.

	SOLUTIONS:
		1.Maybe implementing the database connection as a shared thread object will help prevent this issue		

	Docs: 
		1.http://initd.org/psycopg/docs/connection.html
		2.https://docs.python.org/2/library/threading.html

	DEADLINE:
		4/9/2016


3. Seed.py	

	DELIVERABLES:
		1. seed.py script that launches the following files in order: make-stock-picker.sql, stock_seed.py, price_seed.py, and dividend_seed.py (once it exists)

	DOCS:
		none


	DEADLINE: 4/12/2016		
=======
TASKS IN DECREASING ORDER OF IMPORTANCE -- WITH DEADLINES
=========================================================



1. Postgres connection
	
	DELIVERABLES:
		1. Modified Stock-picker/app.py

	PROBLEM:
		We should be able to setup an @app.beforerequest and @app.teardownrequest in app.py so that a database connection is opened and closed with each route.
		I have not been able to figure out how to make this happen with postgres on flask. Flask does not natively support PG, but the Flask-SQLAlchemy extension
		is the preferred method of handling this. Figure out how to make SQLalchemy open a connection to the stock-picker database.

	SOLUTIONS:
		Read the docs.

	DOCS:
		http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#sql-abstraction-layer
		http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html
		http://flask-sqlalchemy.pocoo.org/2.1/api/
		http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/declarative/api.html
		http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/
		http://docs.sqlalchemy.org/en/latest/core/engines.html			

	
	DEADLINE: 4/10/2016



XXXX
2. HTML/Jinja2 template for viewing a list of all the stocks in the database

	DELIVERABLES:
		1. stock-picker/templates/browse.html
		2. stock-picker/static/css.browse.css
		3. stock-picker/static/js/browse.js
		4. Updates app.py file to reflect new route	
	
	DOCS:
		http://flask.pocoo.org/docs/0.10/tutorial/templates/#layout-html
		
	DEADLINE:
		4/10/2016
XXXX


3. HTML/Jinja2 template for an HTML form that lets users upload a text file for parsing or choose a file from the database

	DELIVERABLES:
		1. stock-picker/templates/pick.html
		2. stock-picker/static/css/pick.css
		3. stock-picker/static/js/pick.js
	        4. Updated app.py file to reflect new route
	DOCS:
		http://flask.pocoo.org/docs/0.10/patterns/wtforms/

	DEADLINE: 4/11/2016
	



4. HTML/Jinja 2 template for viewing the results of the text parsing algorithm
	
	DELIVERABLES:
		1.stock-picker/templates/results.html
		2.stock-picker/static/css/results.css
		3.stock-picker/static/js/results.js
		4.Updated app.py file to reflect new route


	DEADLINE:
		4/12/2016



5.HTML/Jinja 2 templates for site header/footer

	DELIVERABLES:
		1.stock-picker/templates/header.html
		2.stock-picker/static/css/header.css
		3.stock-picker/static/js/header.js
		4.stock-picker/templates/footer.html
		5.stock-picker/static/css/footer.css
		6.stock-picker/static/js/footer.js
	 	


	DEADLINE:
		4/13/2016


6. Setup.py

	DELIVERABLES:
		1. Convert the config/install.sh file into a python script setup.py that sits in the main directory of the flask app
		2. Remove config directory


	DOCS:
		none
	
	DEADLINE:
		4/16/2016



>>>>>>> flask
