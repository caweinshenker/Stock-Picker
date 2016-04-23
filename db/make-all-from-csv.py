import os
import sys

"""
NOTE: this will take a LONG time, but not as long as make-all.py
Populate the database from valid /csvs/ to build a full stock-picker database.
"""

def main(argv):

	print('Initializing database construction and population')
	print('Initializing database "' + argv[1] + '"')
	os.system('createdb ' + argv[1])
	os.system('psql -d ' + argv[1] + ' -f make-stock-picker.sql')

	print('Populating tables from /csvs/')
	os.system('python3 rebuild_database_from_csvs.py')

	print('Done')


main(sys.argv)
