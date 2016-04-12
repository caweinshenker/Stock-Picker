#initial

import csv
from pytrie import SortedStringTrie as trie
#import pytrie

# For initial parsing until we can execute calls on DB

# #Stocks files
# stock_files = ["nasdaq.csv", "amex.csv", "nyse.csv"]

# quickfile = open('tickerList.txt', 'w')
# for stock_file in stock_files:
# 	ticker_list = []
# 	with open(stock_file, 'r') as csvfile:
# 		firstline = True
# 		reader = csv.reader(csvfile, delimiter =",")
# 		for row in reader:
# 			if firstline:
# 				firstline = False
# 				continue
# 			quickfile.write(str(row[0]))
# 			quickfile.write('\n')


# Change this to pulling from db

stringChecker = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ^.'

tickersPresent = []
tickerList = []
tickerDict = {}
push = ''

with open('tickerList.txt', 'r') as tickerFile:
	for line in tickerFile:
		tickerList.append(line.rstrip())

tickerDict = tickerDict.fromkeys(tickerList)
theTrie = trie(tickerDict)


# This should be fixed to do a trailing parse instead of checking word by word
checker = []
with open('test.txt', 'r') as bookFile:
	for line in bookFile:
		for word in line.split():
			checker = []
			for char in word:
				if char.upper() in stringChecker:
					checker.append(char.upper())
			s = ''.join(checker)
			st = s.rstrip()

			if theTrie.has_key(st):
				tickersPresent.append(st)





