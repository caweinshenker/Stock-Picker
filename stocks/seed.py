import datetime
import yahoo_finance
import psycopg2
import pandas as pd

#Open connection to database
conn = psycopg2.connect("dbname=caweinsh_stock_picker user=postgres")
cur = conn.cursor()

#Open CSVs of Stock names, extract stock tickers, and get last 40 years of data from yahoo_finance API
indices = []
nasdaq = "../stocks/nasdaq.csv"
amex   = "../stocks/amex.csv"
nyse   = "../stocks/nyse.csv"
indices.extend(nasdaq, amex, nyse)
for index in indices
	csv = pandas.read_csv(index, delimiter = ",", header = 'infer')
	tickers = csv[:, 0]
	for ticker in tickers:
		stock = Share(ticker)
		today = datetime.datetime.now().strftime("%Y-%d-%m")
		#fix past here
		fortyAgo = datetime.dateime.now.strftime("%
		stock_history = stock.get_historical('
	

