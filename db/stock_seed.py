#import pandas as pd
import time
import multiprocessing
import psycopg2
import getpass
import sys
import csv
sys.path.append('/home/f85/caweinsh/.local/lib/python3.4/site-packages')
from yahoo_finance import *

"""
This file seeds the database with stock entities from csv files
"""

#Stocks files
stock_files   = ["nasdaq.csv", "amex.csv", "nyse.csv"]

def get_ticker_list(cursor, conn):
	"""Open the available lists of stocks, extract their tickers, and call create_stocks

	Params: cursor (database cursor)
	Returns: ticker_list (list of stock tickers)
	"""
	for stock_file in stock_files:
		index_tickers = []
		names_list  = []
		with open(stock_file, 'r') as csvfile:
			firstline = True
			reader = csv.reader(csvfile, delimiter =",")
			for row in reader:
				if firstline:
					firstline = False
					continue
				index_tickers.append(row[0])
				names_list.append(row[1])
		create_stocks(index_tickers, names_list, stock_file.split(".")[0], cursor, conn)
	


def create_stocks(ticker_list, names_list, index, cur, conn):
	"""
	Enter stocks into Stock relation
	params: ticker_list, names_list (company names), index (stock index), cursor (database cursor)
	"""
	for i in range(len(ticker_list)):
		#print("Creating stock entry for: {}".format(ticker_list[i]))
		data = (ticker_list[i], names_list[i], index,)
		if data[0] == "MSG":
			continue
		SQL = "INSERT INTO stock (ticker, company_name, stock_index) VALUES (%s,%s,%s);"
		execute(cur, conn, data, SQL)
	 	
	 
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

def main():
	#Establish database connection
	try:
		conn = psycopg2.connect(database = "caweinsh_stock_picker2", user = "caweinsh", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()
	get_ticker_list(cur, conn)
	cur.close()	
	conn.close()

main()
