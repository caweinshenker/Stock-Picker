from pytrie import SortedStringTrie
from database import Db
from date_parser import Date_Parser
import psycopg2
import sys
import csv
import re
import collections
import random

''' Given a text, investment amount, start date, and end date, generates a stock portfolio from
    that text by finding stock tickers in lines of the text. Inspired by Kurt Vonnegut's
    "The Sirens of Titan." '''

class Parser:

	def __init__(self, text, investment, start_date, end_date):
		self.db = Db()
		self.trie = self.__build_trie() 
		self.text = text
		self.investment = investment
		self.start_date = start_date
		self.end_date = end_date
		#optional for alternate parsing algorithm:
		#self.tickerDict = self.__parse_text_to_tickerDict()
		#self.proportionate_list = self.__build_proportionate_list()
		self.start_value = 0
		self.end_value = 0
		self.portfolio = self.__parse_text()
		self.net_change = self.__net_change()

		self.portfolio_growth = self.__portfolio_growth()

	def __build_trie(self):
		''' 
		Queries the database for stock tickers and places them in a python dictionary
		Constructs a trie from the stock tickers in the database 
		'''
		SQL = "SELECT ticker from stocks;"
		self.db.execute(SQL, None)
		tickerRawData = self.db.fetchall()
		tickerList = [row[0] for row in tickerRawData]
		trie = SortedStringTrie.fromkeys(tickerList, 0)
		return trie
	
	def __parse_text_to_tickerDict(self): 
		'''Read the text line by line. Construct a dictionary tracking ticker occurrences in the text.'''
		tickerDict = {} 
		with open(self.text, "r") as text:
			for line in text:
				line = re.sub('[^A-Za-z0-9]+', '', line)
				line = line.replace(" ", "")
				word = line.upper()
				wordLen = len(word)
				if(len(word) > 0):
					index = 0
					subString = "" + word[index]
					endOfWord = False
					successfulParse = True
					while(len(subString) > 0 & endOfWord == False):
						while(subString in self.trie):
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
	
	def __parse_text(self):
		'''Read the text line by line. Try to construct valid tickers out of lines of text.
                   Buy those tickers until the end of the text is reached, or until money runs out.
                   Return a dictionary of purchased tickers and relevant information'''
		portfolio = {}
		budgetDepleted = False
		with open(self.text, "r") as text:
			budget = self.investment
			for line in text:
				tickerTestIndex = 0
				while ((tickerTestIndex < len(line)) & (budgetDepleted == False)):
					lindex = tickerTestIndex
					curTicker = "" + line[lindex]
					line = re.sub('[^A-Za-z0-9]+', '', line)
					line = line.replace(" ", "")
					line = line.upper()
					testTicker = curTicker
					while((testTicker in self.trie) & (lindex+1 < len(line))):
						print(testTicker)
						curTicker = testTicker
						lindex += 1
						testTicker = testTicker + line[lindex]
					if (curTicker in self.trie):
						selectTickerSatisfyingQuery = "SELECT ticker FROM stock_prices WHERE ticker = %s AND pdate = %s"
						data = (curTicker, self.start_date)
						self.db.execute(selectTickerSatisfyingQuery, data)
						selectTickerSatisfying = self.db.fetchall()
						canBuyTicker = (len(selectTickerSatisfying) > 0)
						data = (curTicker, self.end_date)
						self.db.execute(selectTickerSatisfyingQuery, data)
						selectTickerSatisfying = self.db.fetchall()
						canSellTicker = (len(selectTickerSatisfying) > 0)
						if(canBuyTicker == True & canSellTicker == True):
							curTickerBuyPriceQuery = "SELECT open_price FROM stock_prices WHERE ticker = %s AND pdate = %s"
							data = (curTicker, self.start_date)
							self.db.execute(curTickerBuyPriceQuery, data)
							buyPrice = self.db.fetchall()[0][0]
							curTickerSellPriceQuery = "SELECT open_price FROM stock_prices WHERE ticker = %s and pdate = %s"
							data = (curTicker, self.end_date)
							self.db.execute(curTickerSellPriceQuery, data)
							sellPrice = self.db.fetchall()[0][0]
							if((budget - sellPrice) < 0):
								budgetDepleted = True
								break
							else:
								budget = budget - sellPrice
							if(curTicker in portfolio.keys()):
								portfolio[curTicker][4] += 1
								print(portfolio[curTicker])
							else:
								portfolio[curTicker] = [self.start_date, self.end_date, float(buyPrice), float(sellPrice), 1]
					tickerTestIndex += 1
					print(tickerTestIndex)
		return portfolio
					
				
				
				
		
	def __build_proportionate_list(self):
		'''Build a list out of the tickerDict where ticker entries are proportional to their
                   occurrences in tickerDict, e.g. if tickerDict contains key: AS value: 5, fill the
                   proportionate_list with [AS, AS, AS, AS, AS] '''
		proportionate_list = []
		for key in self.tickerDict:
			count = self.tickerDict[key]
			while (count > 0):
				count -= 1
				proportionate_list.append(key)
		return proportionate_list


	
	def __make_portfolio(self):
		'''Builds a stock portfolio by selecting randomly from a list of stock tickers
                   and purchasing until the budget is expended'''	
		portfolio = {}
		budget = self.investment
		canBuyMoreStocks = True
		while((budget > 0) and (canBuyMoreStocks)):
			randomTicker = random.choice(self.proportionate_list)
			randomTicker = re.sub('[^A-Za-z0-9]+', '', randomTicker)
			curTickerBuyDate = self.start_date
			selectTickerSatisfyingQuery = "SELECT ticker FROM stock_prices WHERE ticker = %s AND pdate = %s"
			data = (randomTicker, curTickerBuyDate)
			self.db.execute(selectTickerSatisfyingQuery, data)
			selectTickerSatisfying = self.db.fetchall()
			canBuyTicker = (len(selectTickerSatisfying) > 0)
			while(canBuyTicker == False):
				randomTicker = random.choice(self.proportionate_list)
				randomTicker = re.sub('[^A-Za-z0-9]+', '', randomTicker)
				data = (randomTicker, curTickerBuyDate)
				self.db.execute(selectTickerSatisfyingQuery, data)
				selectTickerSatisfying = self.db.fetchall()
				canBuyTicker = (len(selectTickerSatisfying) > 0)
			curTickerSellDate = self.end_date
			curTickerBuyPriceQuery = "SELECT open_price FROM stock_prices WHERE ticker = %s AND pdate = %s"
			data = (randomTicker, curTickerBuyDate)
			self.db.execute(curTickerBuyPriceQuery, data)
			buyPrice = self.db.fetchall()[0][0]
			curTickerSellPriceQuery = "SELECT open_price FROM stock_prices WHERE ticker = %s and pdate = %s"
			data = (randomTicker, curTickerSellDate)
			self.db.execute(curTickerSellPriceQuery, data)
			sellPrice = self.db.fetchall()[0][0]
			if((budget - sellPrice) < 0):
				canBuyMoreStocks = False
			else:
				budget = budget - sellPrice
				if(randomTicker in portfolio.keys()):
					portfolio[randomTicker][4] += 1
				else:
					portfolio[randomTicker] = [curTickerBuyDate, curTickerSellDate, float(buyPrice), float(sellPrice), 1]
		
		return portfolio
		

	def __net_change(self):
		'''Return the net change of the portfolio'''
		self.start_value = 0
		self.end_value = 0
		for ticker in self.portfolio:
			self.start_value += self.portfolio[ticker][2] * self.portfolio[ticker][4]
			self.end_value += self.portfolio[ticker][3] * self.portfolio[ticker][4]
		self.net_change = self.end_value - self.start_value
		

	def __portfolio_growth(self):
		'''Return a dictionary of portfolio values on dates between start_date and end_date'''
		dp = Date_Parser(self.start_date, self.end_date)
		date_range = dp.get_date_range()
		value_at_date = {} 
		SQL = "Select pdate, open_price FROM stock_prices WHERE ticker = %s AND pdate = %s ORDER BY pdate;" 			
		for date in date_range:
			portfolio_value = 0
			for ticker in self.portfolio.keys():
				data = (ticker, date)
				self.db.execute(SQL, data)
				results = self.db.fetchall()
				if len(results) > 0:
					open_price = results[0][1]
					portfolio_value += float(open_price) * self.portfolio[ticker][4]
			if portfolio_value != 0:				
				value_at_date[results[0][0]] = portfolio_value
			else:
				date_range.remove(date) 
		return value_at_date		
		
