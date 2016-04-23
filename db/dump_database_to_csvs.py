import sys
import csv
import psycopg2
import getpass

def main():
	try:
		conn = psycopg2.connect(database = "max_stock", user = "maxmir", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
		exit
	cur = conn.cursor()

	#dump stock price data into csv
	SQLQuery = "select * from stock_prices"
	
	try:
		cur.execute(SQLQuery)
	except Exception as e:
		print(str(e))
		pass

	stockData = cur.fetchall()
	writeFileName = "csvs/stock_prices.csv"
	with open(writeFileName, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for entry in stockData:
			csvwriter.writerow([entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]])
	
	#dump stock volume data into csv
	SQLQuery = "select * from stock_volumes"

	try:
		cur.execute(SQLQuery)
	except Exception as e:
		print(str(e))
		pass

	stockData = cur.fetchall()
	writeFileName = "csvs/stock_volumes.csv"		
	with open(writeFileName, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for entry in stockData:
			csvwriter.writerow([entry[0], entry[1], entry[2]])

	#dump stocks table into csv
	SQLQuery = "select * from stocks"
	
	try:
		cur.execute(SQLQuery)
	except Exception as e:
		print(str(e))
		pass

	stockData = cur.fetchall()
	writeFileName = "csvs/stocks.csv"
	with open(writeFileName, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for entry in stockData:
			csvwriter.writerow([entry[0], entry[1], entry[2], entry[3], entry[4]])

	#dump dividends table into csv
	SQLQuery = "select * from stock_dividends"

	try:
		cur.execute(SQLQuery)
	except Exception as e:
		print(str(e))
		pass

	stockData = cur.fetchall()
	writeFileName = "csvs/stock_dividends.csv"
	with open(writeFileName, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for entry in stockData:
			csvwriter.writerow([entry[0], entry[1], entry[2]])


	cur.close()
	conn.close()
main()
