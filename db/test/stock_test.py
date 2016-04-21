import unittest
import sys

class StockTest(unittest.TestCase):
	def setUp(self):
		try:
		self.conn = psycopg2.connect(database = "caweinsh_stock_picker2", user = "caweinsh", password = getpass.getpass())
		except StandardError as e:
			print(str(e))
			sys.exit(0)
	self.cur = conn.cursor()

	def tearDown(self):
		self.cur.close()
		self.conn.close()
	
	#Check all stocks are in database
	def count_test(self):
		self.cur.execute("SELECT count(ticker) FROM stock;")
		self.assertEqual(len(self.cur), 6701)

	#Check for no duplicates
	def no_dups_test(self):
		count_all = len(self.cur.execute("SELECT ticker FROM stock;")
		count_distinct = len(self.cur.execute("SELECT distinct(ticker) FROM stock;")
		self.assertEqual(countall, count_distinct)

if __name__ == '__main__':
	unittest.main()
