import os
import sys

"""
NOTE: this will take a LONG time, but not as long as make-all.py
Populate the database from valid /csvs/ to build a full stock-picker database.
argv[1] = database name
argv[2] = username
"""

def main(argv):

	assert(len(argv) == 3), "incorrect query. try: 'python setup.py DATABASENAME USERNAME'"

	print("Installing requisite dependencies")
	os.system("chmod u+x install.sh")

	print('Initializing database construction and population')
	print('Initializing database "' + argv[1] + '" for user: ' + argv[2])
	os.system('createdb ' + argv[1])
	os.system('psql -d ' + argv[1] + ' -f db/make-stock-picker.sql')

	print('Populating tables from /csvs/')
	os.system('python3 db/rebuild_database_from_csvs.py ' + argv[1] + ' ' + argv[2])

	print('Done')


main(sys.argv)
