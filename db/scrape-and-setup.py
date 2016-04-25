import os
import sys

"""
NOTE: this will take a LONG, LONG time
Run all the seed files to build a full stock-picker database from fresh Yahoo! Finance data.
When run from command line, first argument argv[1] = database name
                            second argument argv[2] = username for database
"""

def main(argv):

	assert(len(argv) == 3), "incorrect query. try: 'python scrape-and-setup.py DATABASENAME USERNAME'"

	print("Installing requisite dependencies")
	os.system("chmod u+x install.sh")

	print('Initializing database construction and population')
	print('Initializing database "' + argv[1] + '"' + ' for user: ' + argv[2])
	os.system('createdb ' + argv[1])
	os.system('psql -d ' + argv[1] + ' -f db/make-stock-picker.sql')
	
	print('Populating stock table')
	os.system('python3 db/stock_seed.py ' + argv[1] + ' ' + argv[2])

	print('Populating stock price table with 10 years of data')
	os.system('nohup python3 db/price_seed.py 2006-04-04 2016-04-04 ' + argv[1] + ' ' + argv[2])

	print('Populating dividend table with 10 years of data')
	os.system('python3 db/get_dividend_csv.py')
	os.system('python3 db/dividend_seed.py ' + argv[1] + ' ' + argv[2])

	print('Done')


main(sys.argv)
