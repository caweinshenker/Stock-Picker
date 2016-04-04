#import pandas as pd
import time
import multiprocessing
import subprocess
from datetime import date
import psycopg2
import getpass
import sys
import csv
sys.path.append('/home/f85/caweinsh/.local/lib/python3.4/site-packages')
from yahoo_finance import *

"""
This file seeds the database with data from Yahoo! Finance API
Last update: 4/4/2014-4/4/2016
"""

#Stocks files
stock_files   = ["nasdaq.csv", "amex.csv", "nyse.csv"]

def get_ticker_list(cursor, conn):
	"""Open the available lists of stocks, extract their tickers, and call create_stocks

	Params: cursor (database cursor)
	Returns: ticker_list (list of stock tickers)
	"""
	for stock_file in stock_files:
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
	return(ticker_list)
	
	
	 
def get_history(ticker_list, cur, conn, argv):
	"""
	Use Yahoo API to get stock data for date range specified in 
	argv and pass data to create_stock_price
        Params: ticker_list, names_list (stock names), index (stock index), 
	cursor (database cursor)
	"""
	for ticker in ticker_list:
		#Deal w/ data-cleaning issue
		if ticker == "MSG" or ticker == "PBB":
			continue
		try:
			stock = Share(ticker)
		except AttributeError:
			continue
		start_date = argv[1]
		end_date = argv[2]
		history = stock.get_historical(start_date, end_date)
		create_stock_price(ticker, history, cur, conn)


def create_stock_price(ticker, history, cur, conn):
	"""
	Enter stock prices into Stock_price relation
	params: ticker, history (list of hashes, each hash contains data on a given date for the given stock), cur, 
	"""
	#print("Creating stock price entry for: {}".format(ticker))
	for date in history:
		day = date['Date']
		open_price = date['Open']
		close_price = date['Close']
		data = (ticker, day, float(open_price), float(close_price))
		print(str(data))
		SQL = "INSERT INTO stock_price(ticker, pdate, open_price, close_price) VALUES (%s, %s, %s, %s);"
		execute_insert(cur, conn, data, SQL)
	conn.commit()

def execute_insert(cur, conn, data, SQL):
	try:
		cur.execute(SQL, data)
	except psycopg2.IntegrityError as e:
		print(str(e) + "\n")
		print(str(data))
		sys.exit(0)
	except psycopg2.InternalError as e:
		print(str(e))
		sys.exit(0)
	except psycopg2.ProgrammingError as e:
		print(str(e))
		sys.exit(0)

def process_launch_stocks(processes, ticker_list, cur, conn, argv):
	"""
	Pass the ticker list in chunks to the API for processing.
	Leverage multiprocessing.
	"""
	chunk_size = int(len(ticker_list) / processes)
	processes = []
	for i in range(0, len(ticker_list), chunk_size):
		chunk = ticker_list[i: i + chunk_size]
		p = multiprocessing.Process(target=get_history, args=(chunk, cur, conn, argv))
		processes.append(p)
		p.start()
	for process in processes:
		process.join()
	#DO NOT COMMIT BEFORE ALL THREADS FINISH. MONDO PSQL PROBLEMS WILL HAPPEN


def main(argv):
	try:
		conn = psycopg2.connect(database = "caweinsh_stock_picker2", user = "caweinsh", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()
	ticker_list = get_ticker_list(cur, conn)
	#Launch multithreading to handle  API data
	process_launch_stocks(24, ticker_list, cur, conn, argv)
	cur.close()	
	conn.close()

main(sys.argv)