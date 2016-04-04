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
		create_stocks(ticker_list, names_list, stock_file.split(".")[0], cursor, conn)
	return(ticker_list)
	


def create_stocks(ticker_list, names_list, index, cur, conn):
	"""
	Enter stocks into Stock relation
	params: ticker_list, names_list (company names), index (stock index), cursor (database cursor)
	"""
	for i in range(len(ticker_list)):
		#print("Creating stock entry for: {}".format(ticker_list[i]))
		data = (ticker_list[i], names_list[i], index,)
		if data[0] == "MSG":
			#print("NO MSG")
			continue
		SQL = "INSERT INTO stock (ticker, company_name, stock_index) VALUES (%s,%s,%s);"
		execute(cur, conn, data, SQL)
	conn.commit()
	 
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
	#print("Creating stock price entry for: {}".format(ticker))
	for date in history:
		day = date['Date']
		open_price = date['Open']
		close_price = date['Close']
		data = (ticker, day, float(open_price), float(close_price))
		#print(str(data))
		SQL = "INSERT INTO stock_price(ticker, pdate, open_price, close_price) VALUES (%s, %s, %s, %s);"
		execute(cur, conn, data, SQL)
	conn.commit()


#def create_dividends(ticker_list, cur, conn):
	#SQL = "INSERT INTO stock_dividend(ticker
	#for i in range(ticker_list):
		
	

def execute(cur, conn, data, SQL):
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

def process_launch_stocks(processes, ticker_list, cur, conn):
	"""
	Pass the ticker list in chunks to the API for processing.
	Leverage multiprocessing.
	"""
	chunk_size = int(len(ticker_list) / processes)
	processes = []
	for i in range(0, len(ticker_list), chunk_size):
		chunk = ticker_list[i: i + chunk_size]
		p = multiprocessing.Process(target=get_history, args=(chunk, cur, conn,))
		processes.append(p)
		p.start()
	for process in processes:
		process.join()


def process_launch_dividends(processes, ticker_list, cur, conn):
	chunk_size = int(len(ticker_list) / processes)
	processes = []
	for i in range(0, len(ticker_list), chunk_size):
		chunk = ticker_list[i: i + chunk_size]
		p = multiprocessing.Process(target=create_dividends, args=(chunk, cur, conn,))
		processes.append(p)
		p.start()
	for process in processes:
		process.join()



def main():
	#Rebuild database
	#bashCommand = "psql -d caweinsh_stock_picker -f make-stock-picker.sql"
	#process = subprocess.Popen(bashCommand.split(), stdout = subprocess.PIPE)
	#output = process.communicate()[0]
	#Establish database connection
	try:
		conn = psycopg2.connect(database = "caweinsh_stock_picker", user = "caweinsh", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()
	ticker_list = get_ticker_list(cur, conn)
	#Launch multithreading to handle  API data
	process_launch_stocks(24, ticker_list, cur, conn)
	cur.close()	
	conn.close()

main()
