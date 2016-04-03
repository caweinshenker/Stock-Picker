import numpy as np
import pandas as pd
import datetime as dt
import psycopg2
import getpass
import sys
from yahoo_finance import *


"""
This file seeds the database with data from Yahoo! Finance API
"""

#Stocks files
stock_files   = []
nasdaq = "nasdaq.csv"
amex   = "amex.csv"
nyse   = "nyse.csv"
stock_files.extend(nasdaq, amex, nyse)


def get_ticker_list(cursor):
"""
	Open the available lists of stocks, extract their tickers, and call create_stocks

	Params: cursor (database cursor)
	Returns: ticker_list (list of stock tickers)
"""

	for stock_file in stock_files:
        	stock_csv = pd.read_csv(stock_file, sep =",", header = 0)
        	ticker_list = stock_csv[:,0]
		names_list = stock_csv[:, 1]
		create_stocks(ticker_list, names_list, stock_file.split(".")[0], cursor)
       	return ticker_list


def create_stocks(ticker_list, names_list, index, cursor):
"""
	Enter stocks into Stock relation
	params: ticker_list, names_list (company names), index (stock index), cursor (database cursor)
"""
	for i in range(len(ticker_list)):
		cur.execute("INSERT INTO Stock (ticker, company_name, index) VALUES (%s, %s, %s)".format(ticker_list[i], names_list[i], index))
	
	 
def get_history(ticker_list, cur):
"""
	Use Yahoo API to get stock data for past 40 years and pass data to create_stock_price
        Params: ticker_list, names_list (stock names), index (stock index), cursor (database cursor)
"""
	for ticker in ticker_list:
		stock = Share(ticker)
		today = datetime.today()
		today_year, today_month, today_day = today.year, today.month, today.day
		history_year, history_month, history_day  = today.year - 40, today.month, today.day
		today_string = "%s-%s-%s".format(today_year, today_month, today_day)
		history_string = "%s-%s-%s".format(history_year, history_month, history_day)
		history = stock.get_historical(history_string, today_string)
		create_stock_price(ticker, history, cur, conn)


def create_stock_price(ticker, history, cur):
"""
	Enter stock prices into Stock_price relation
	params: ticker, history (list of hashes, each hash contains data on a given date for the given stock), cur, 
"""
	for date in history:
		day = date['Date']
		open_price = date['Open']
		close_price = date['Close']
		cur.execute("INSERT INTO Stock (ticker, date, open_price, close_price) VALUES (%s, %s, %d, %d)".format(ticker, date, open_price, close_price)
		 
		
		
	

def main():
	#Establish database connection
	try:
		conn = psycopg2.connect(database = "caweinsh_stock_picker", user = "caweinsh", password = getpass.getpass() )
	except StandardError, e:
		print(str(e))
		exit
	cur = connection.cursor()
	ticker_list = get_ticker_list(cur)
	get_history(ticker_list, cur)	
	conn.close()


