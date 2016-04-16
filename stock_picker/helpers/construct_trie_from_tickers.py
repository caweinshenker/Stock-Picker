from pytrie import SortedStringTrie
import psycopg2
import getpass
import sys
import csv

''' Constructs a trie from the stock tickers in the database '''

def query_database_for_tickers():
	''' Queries the database for stock tickers and places them in a python dictionary '''

	try:
		conn = psycopg2.connect(database = "max_stock", user = "maxmir", password = getpass.getpass())
	except StandardError as e:
		print(str(e))
	cur = conn.cursor()
	query = "SELECT * FROM stock"

	try:
		cur.execute(query)
	except Exception:
		print("You're Exceptional")

	tickerRawData = cur.fetchall()
	tickerList = []
	for entry in tickerRawData:
		tickerList.append(entry[0])
	trie = SortedStringTrie.fromkeys(tickerList, 0)
	cur.close()
	conn.close()
	return trie
'''
def main():
	tickerTrie = query_database_for_tickers()

main()
'''
