#import pandas as pd
import time
import multiprocessing
import psycopg2
import getpass
import sys
import csv
import yahoo_finance
from yahoo_finance import *

"""
This file seeds the database with data from Yahoo! Finance API

UPDATED: 2013-04-04 2016-04-04
"""

#Stocks files
stock_files   = ["csvs/nasdaq.csv", "csvs/amex.csv", "csvs/nyse.csv"]

def get_ticker_list(cursor, conn):
	"""Open the available lists of stocks, extract their tickers, and call create_stocks

	Params: cursor (database cursor)
	Returns: ticker_list (list of stock tickers)
	"""
	ticker_list = []
	for stock_file in stock_files:
		with open(stock_file, 'r') as csvfile:
			firstline = True
			reader = csv.reader(csvfile, delimiter =",")
			for row in reader:
				if firstline:
					firstline = False
					continue
				ticker_list.append(row[0])
	return(ticker_list)
	


 
def get_history(ticker_list, cur, conn, argv):
	"""
	Use Yahoo API to get stock data for past 40 years and pass data to create_stock_price
        Params: ticker_list, names_list (stock names), index (stock index), cursor (database cursor)
	"""
	for ticker in ticker_list:
		#Deal w/ data-cleaning issue
		if ticker == "MSG":
			continue
		date1 = argv[1]
		date2 = argv[2]
		try:
			stock = Share(ticker)
		except Exception as e:
			print(str(e))
			continue
		try:
			history = stock.get_historical(str(date1), str(date2))
		except Exception as e:
			print(e)
			continue
		create_stock_price_volumes(ticker, history, cur, conn)

def create_stock_price(ticker, history, cur, conn):
	"""
	Enter stock prices into stock_price relation and volumes into volume relation
	params: ticker, history (list of hashes, each hash contains data on a given date for the given stock), cur, 
	"""
	#print("Creating stock price entry for: {}".format(ticker))
	for date in history:
		try:
			day = date['Date']
		except Exception as e:
			print(str(e))
			continue
		try:
			open_price = date['Open']
		except Exception as e:
			print(str(e))
			continue
		try:
			close_price = date['Close']
		except Exception as e:
			print(str(e))
			continue
		try:
			high = date['High']
		except Exception as e:
			print(str(e))
			continue
		try:
			low = date['Low']
		except Exception as e:
			print(str(e))
			continue
		try: 
			volume = date['Volume']
		exept Exception as e:
			print(str(e))
			continue
		price_data = (ticker, day, float(open_price), float(close_price), float(high), float(low))
		volume_data = (ticker, day, volume)
		price_SQL = "INSERT INTO stock_prices(ticker, pdate, open_price, close_price, high, low) VALUES (%s, %s, %s, %s, %s, %s);"
		volume_SQL = "INSERT INTO stock_volumes(ticker, vdate, volume) VALUES (%s, %s, %d);"
		execute(cur, conn, price_data, price_SQL)
		execute(cur, conn, volume_data, volume_SQL)	
	conn.commit()
	
def execute(cur, conn, data, SQL):
	try:
		cur.execute(SQL, data)
	except Exception as e:
		print(str(e))
		pass

def process_launch_stocks(processes, ticker_list, cur, conn, argv):
	"""
	Pass the ticker list in chunks to the API for processing.
	Leverage multiprocessing.
	"""
	chunk_size = int(len(ticker_list) / processes)
	processes = []
	for i in range(0, len(ticker_list), chunk_size):
		chunk = ticker_list[i: i + chunk_size]
		p = multiprocessing.Process(target=get_history, args=(chunk, cur, conn,argv,))
		processes.append(p)
		p.start()
	for process in processes:
		process.join()

def main(argv):
	try:
		conn = psycopg2.connect(database = "caweinsh_sp3", user = "caweinsh", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()
	ticker_list = get_ticker_list(cur, conn)
	#Launch multithreading to handle  API data
	#process_launch_stocks(24, ticker_list, cur, conn, argv)
	get_history(ticker_list, cur, conn, argv)
	cur.close()	
	conn.close()
	print("Complete: " + str(argv[1]) + " " +  str(argv[2]))

main(sys.argv)
