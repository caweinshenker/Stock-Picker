import time
import multiprocessing
import psycopg2
import getpass
import sys
import csv
from yahoo_finance import *

"""
MUST RUN IN PYTHON3!!!!

This file seeds the database with stock entities from csv files
"""

#Stocks files
stock_files   = ["csvs/nasdaq.csv", "csvs/amex.csv", "csvs/nyse.csv"]

def get_tickers_indices_names(cursor, conn):
	"""Open the available lists of stocks, extract their tickers, and call create_stocks

	Params: cursor (database cursor)
	Returns: ticker_list (list of stock tickers)
	"""
	tickers = []
	indices = []
	names = []
	for stock_file in stock_files:
		with open(stock_file, 'r') as csvfile:
			firstline = True
			reader = csv.reader(csvfile, delimiter =",")
			for row in reader:
				if firstline:
					firstline = False
					continue
				tickers.append(row[0])
				indices.append(stock_file.split(".")[0].split("/")[1])
				names.append(row[1])
	return(tickers, indices, names)	


def create_stock(ticker, name, index,  info, cur, conn):
	"""
	Enter stocks into stocks relation
	params: ticker_list, names_list (company names), index (stock index), cursor (database cursor)
	"""
	if ticker == "MSG":
		return
	start = None
	end = None
	try: 
		start = info['start']
	except Exception as e:
		pass
	try:	
		end = info['end']
	except Exception as e:
		pass
	if ((start != None) and (end != None)) and ('NaN' in start or 'NaN' in end):
		start = None
		end = None
	data = (ticker, index, name, start, end)
	SQL = "INSERT INTO stocks (ticker, stock_index, company_name, start_date, end_date) VALUES (%s, %s, %s, %s, %s);"
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
		conn = psycopg2.connect(database = "caweinsh_sp3", user = "caweinsh", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		sys.exit(1)
	cur = conn.cursor()
	tickers_indices_names = get_tickers_indices_names(cur, conn)
	tickers = tickers_indices_names[0]
	indices = tickers_indices_names[1]
	names = tickers_indices_names[2]
	for i in range(len(tickers)):
		try:
			stock = Share(tickers[i])
		except Exception as e:
			continue
		try:
			info = stock.get_info()
		except Exception as e:
			continue
		create_stock(tickers[i], names[i], indices[i], info, cur, conn)
		conn.commit()	
	cur.close()	
	conn.close()

main()
