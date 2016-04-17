import construct_trie_from_tickers as trieMaker
import psycopg2
import getpass
import sys
import csv
import re


def parse_text(text, trie):
	tickerDict = {}
	with open(text, "r") as text:
		for line in text:
			line = re.sub('[^A-Za-z0-9]+', '', line)
			line = line.replace(" ", "")		
			#for word in line.split(" "):
			word = line.upper()
			wordLen = len(word)
			if(len(word) > 0):
				index = 0
				subString = "" + word[index]
				endOfWord = False
				successfulParse = True
				while(len(subString) > 0 & endOfWord == False):
					while(subString in trie):
						successfulParse = True
						if (subString in tickerDict):
							tickerDict[subString] += 1
						else:
							tickerDict[subString] = 1
						if(index < (wordLen - 1)):
							index += 1
							subString = subString + word[index]
						elif (index == (wordLen- 1)):
							subString = ""
							endOfWord = True
					if(endOfWord == True):
						subString = ""
					else:
						if(successfulParse == False):
							if(index < (wordLen - 1)):
								index += 1
							else:
								endOfWord = True
						subString = "" + word[index]
					successfulParse = False
	return tickerDict


def main():
	text = "../uploads/flatland.txt"
	tickerTrie = trieMaker.query_database_for_tickers()
#	print(tickerTrie)
	portfolioList = parse_text(text, tickerTrie)
#	print(portfolioList)
	

main()

