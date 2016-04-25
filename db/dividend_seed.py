#import pandas as pd
import time
import multiprocessing
import subprocess
import psycopg2
import getpass
import sys
import csv
"""
This file seeds the database with dividend data obtained with get_dividend_csv. Then, it parses the .csv file and adds it to a list.
Finally, list information is added to the database. Run it with commandline argv[1] = database name and
argv[2] = username for database
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
	''' put data from our generated list into the database '''
	for entry in dividend_data:
		SQL = "INSERT INTO stock_dividends(ticker, ddate, price) VALUES (%s, %s, %s)"
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
		conn = psycopg2.connect(database = argv[1], user = argv[2], password = getpass.getpass())
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
