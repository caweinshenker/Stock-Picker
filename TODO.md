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
