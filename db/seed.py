#import pandas as pd
import time
from datetime import date
import psycopg2
import getpass
import sys
import csv
from yahoo_finance import *

"""
This file seeds the database with data from Yahoo! Finance API
"""

#Stocks files
stock_files   = ["nasdaq.csv", "amex.csv", "nyse.csv"]

def get_ticker_list(cursor, conn):
	"""Open the available lists of stocks, extract their tickers, and call create_stocks

	Params: cursor (database cursor)
	Returns: ticker_list (list of stock tickers)
	"""
	for stock_file in stock_files:
                #stock_csv = pd.read_csv(stock_file, sep =",", header = 0)
		ticker_list = []
		names_list = []
		with open(stock_file, 'r') as csvfile:
			firstline = True
			reader = csv.reader(csvfile, delimiter =",")
			for row in reader:
				if firstline:
					firstline = False
					continue
				ticker_list.append(row[0])
				names_list.append(row[1])
		#ticker_list = stock_csv[:,0]
                #names_list = stock_csv[:, 1]
		create_stocks(ticker_list, names_list, stock_file.split(".")[0], cursor, conn)
	return(ticker_list)
	


def create_stocks(ticker_list, names_list, index, cur, conn):
	"""
	Enter stocks into Stock relation
	params: ticker_list, names_list (company names), index (stock index), cursor (database cursor)
	"""
	for i in range(len(ticker_list)):
		data = (ticker_list[i], names_list[i], index,)
		if data[0] == "MSG":
			print("NO MSG")
			continue
		SQL = "INSERT INTO stock (ticker, company_name, stock_index) VALUES (%s,%s,%s);"
		execute(cur, conn, data, SQL)
	
	 
def get_history(ticker_list, cur, conn):
	"""
	Use Yahoo API to get stock data for past 40 years and pass data to create_stock_price
        Params: ticker_list, names_list (stock names), index (stock index), cursor (database cursor)
	"""
	for ticker in ticker_list:
		#Deal w/ data-cleaning issue
		if ticker == "MSG":
			print("NO MSG")
			continue
		stock = Share(ticker)
		today = date.today()
		today_year, today_month, today_day = today.year, today.month, today.day
		history_year, history_month, history_day  = today.year - 40, today.month, today.day
		today_string = "{}-{}-{}".format(today_year, today_month, today_day)
		history_string = "{}-{}-{}".format(history_year, history_month, history_day)
		history = stock.get_historical(history_string, today_string)
		create_stock_price(ticker, history, cur, conn)


def create_stock_price(ticker, history, cur, conn):
	"""
	Enter stock prices into Stock_price relation
	params: ticker, history (list of hashes, each hash contains data on a given date for the given stock), cur, 
	"""
	for date in history:
		day = date[u'Date']
		open_price = date[u'Open']
		close_price = date[u'Close']
		data = (ticker, date, float(open_price), float(close_price))
		print(str(data))
		SQL = "INSERT INTO stock(ticker, date, open_price, close_price) VALUES (%s, %s, %s, %s);"
		execute(cur, conn, data, SQL)
	

def execute(cur, conn, data, SQL):
	#print(str(data))
	try:
		cur.execute(SQL, data)
	except psycopg2.IntegrityError as e:
		print(str(e) + "\n")
		print(str(data))
	except psycopg2.InternalError as e:
		print(str(e))
	except psycopg2.ProgrammingError as e:
		print(str(e))
		exit	


def main():
	#Establish database connection
	try:
		conn = psycopg2.connect(database = "caweinsh_stock_picker", user = "caweinsh", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()
	ticker_list = get_ticker_list(cur, conn)
	get_history(ticker_list, cur, conn)	
	conn.close()

main()
