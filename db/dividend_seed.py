#import pandas as pd
import time
import multiprocessing
import subprocess
import psycopg2
import getpass
import sys
import csv
"""
This file seeds the database with data from dividend data from the Quandl API

UPDATED: 2013-04-04 2016-04-04
"""

def parse_dividend_csv(filename):
	''' get data from the dividend csv in a usable format '''
	dividend_data = []

	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = ",")
		ticker = "DDD" #first ticker is DDD
		for row in reader:
			if ("end_of_data" in row[0]):
				ticker = row[0]
				ticker = ticker.replace("end_of_data", "")
				ticker = ticker.replace("Date", "")
			else:
				dividend_data.append((ticker, row[0], row[1]))
	return dividend_data

def input_data_to_database(dividend_data, cur, conn):
	for entry in dividend_data:
		#SQL = "select ticker from dividend_price where ticker = (%s)"
		#execute(cur, conn, entry[0], SQL) 
		#if len(cur.fetchall() == 0):
		SQL = "INSERT INTO stock_dividend(ticker, ddate, price) VALUES (%s, %s, %s)"
		execute(cur, conn, entry, SQL)
		conn.commit()
		


def execute(cur, conn, data, SQL):
	try:
		cur.execute(SQL, data)
	except Exception as e:
		print(str(e))
		pass

def main(argv):
	
	try:
		conn = psycopg2.connect(database = "caweinsh_sp3", user = "caweinsh", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()
	dividend_data = parse_dividend_csv("csvs/dividend_info.csv")
	input_data_to_database(dividend_data, cur, conn)	
	cur.close()	
	conn.close()
	print("Complete: " + str(argv[1]) + " " +  str(argv[2]))
main(sys.argv)
