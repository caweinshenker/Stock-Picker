import construct_trie_from_tickers as trieMaker
import psycopg2
import getpass
import sys
import csv

def parse_text(text, trie):
''' given a text location and a trie of tickers, returns a dictionary where the keys are tickers
    and the values are the occurences of the ticker within the words of the text '''
	tickerDict = {}
	with open(text, "r") as text:
		for line in text:
			for word in line.split(" "):
				word = word.upper()
				wordLen = len(word)
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

'''	
def main():
	text = "../texts/test.txt"
	tickerTrie = trieMaker.query_database_for_tickers()
	print(tickerTrie)
	portfolioList = parse_text(text, tickerTrie)
	print(portfolioList)
	

main()
'''
