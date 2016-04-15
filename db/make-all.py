import os
import sys



def main(argv):

	print('Initializing database construction and population')
	print('Initializing database "' + argv[1] + '"')
	os.system('createdb ' + argv[1])
	os.system('psql -d ' + argv[1] + ' -f make-stock-picker.sql')
	
	print('Populating stock table')
	os.system('python3 stock_seed.py')

	print('Populating stock price table')
	os.system('nohup python3 price_seed.py 1996-04-04 2016-04-04')

	print('Populating dividend table')
	os.system('python3 dividend_seed.py')

	print('Done')


main(sys.argv)
