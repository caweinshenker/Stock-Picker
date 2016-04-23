import sys
import csv
import psycopg2
import getpass
import os

''' Populates database tables from /csvs/ '''

def main(argv):

	dbName = argv[1]
	try:
		conn = psycopg2.connect(database = dbName, user = "maxmir", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()

	#create stocks
	readFileName = "csvs/stocks.csv"
	with open(readFileName, 'r', newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		SQLQuery = "INSERT INTO stocks(ticker, stock_index, company_name, start_date, end_date) VALUES (%s, %s, %s, %s, %s);"
		for line in csvreader:
			if(line[3] == ""): 
				line[3] = None
			if(line[4] == ""): 
				line[4] = None
			data = (line[0], line[1], line[2], line[3], line[4],)
			try:
				cur.execute(SQLQuery, data)
			except psycopg2.IntegrityError as e:
				print(str(e) + "\n")
				print(str(data))
				break
			except psycopg2.InternalError as e:
				print(str(e))
				break
			except psycopg2.ProgrammingError as e:
				print(str(e))
				break
			except Exception as e:
				print(str(e))
				break
	conn.commit()
	#create stock_prices
	readFileName = "csvs/stock_prices.csv"
	with open(readFileName, 'r', newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for line in csvreader:
			data = (line[0], line[1], line[2], line[3], line[4], line[5])
			SQLQuery = "INSERT INTO stock_prices(ticker, pdate, open_price, close_price, high, low) VALUES (%s, %s, %s, %s, %s, %s);"
			try:
				cur.execute(SQLQuery, data)
			except Exception as e:
				print(str(e))
				continue

	conn.commit()
	#create stock_volumes
	readFileName = "csvs/stock_volumes.csv"
	with open(readFileName, 'r', newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for line in csvreader:
			data = (line[0], line[1], line[2])
			SQLQuery = "INSERT INTO stock_volumes(ticker, vdate, volume) VALUES (%s, %s, %s);"
			try:
				cur.execute(SQLQuery, data)
			except Exception as e:
				print(str(e))
				continue
	conn.commit()
	#create stock_dividends
	readFileName = "csvs/stock_dividends.csv"
	with open(readFileName, 'r', newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for line in csvreader:
			data = (line[0], line[1], line[2])
			SQLQuery = "INSERT INTO stock_dividends(ticker, ddate, price) VALUES (%s, %s, %s);"
			try:
				cur.execute(SQLQuery, data)
			except Exception as e:
				print(str(e))
				continue

	conn.commit()	
	cur.close()
	conn.close()

main(sys.argv)
