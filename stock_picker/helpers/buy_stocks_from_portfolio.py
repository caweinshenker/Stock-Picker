import parse_text_for_portfolio as textPortfolio
import construct_trie_from_tickers as trieMaker
import psycopg2
import getpass
import sys
import csv
import re
import random

def execute(cur, conn, data, SQL):
	try:
		cur.execute(SQL, data)
		return cur
	except Exception as e:
		print(str(e))
		pass
	return cur

def make_portfolio(tickerDict, capitalInvested, buyDate, sellDate):
	portfolioDict = {}
	try:
		conn = psycopg2.connect(database = "max_stock", user = "maxmir", password = getpass.getpass())
	except Exception as e:
		print(str(e))
	cur = conn.cursor()
	budget = capitalInvested
	canBuyMoreStocks = True
	while((budget > 0) and (canBuyMoreStocks)):
		randomTicker = random.choice(list(tickerDict.keys()))
		randomTicker = re.sub('[^A-Za-z0-9]+', '', randomTicker)
		#print(randomTicker)
		curTickerBuyDate = buyDate
		#print(curTickerBuyDate)
		
		selectTickerSatisfyingQuery = "SELECT ticker FROM stock_prices WHERE ticker = %s AND pdate = %s"
		data = (randomTicker, curTickerBuyDate)
		selectTickerSatisfying = execute(cur, conn, data, selectTickerSatisfyingQuery)
		selectTickerSatisfying = selectTickerSatisfying.fetchall()
		#print("List of tickers: " + str(selectTickerSatisfying))
		canBuyTicker = (len(selectTickerSatisfying) > 0)
		#print(len(selectTickerSatisfying))
		#print(canBuyTicker)
		'''
		checkTickerBuyQuery = "%s IN (SELECT ticker FROM stock_prices WHERE ticker = %s AND pdate = %s)"
		data = (randomTicker, randomTicker, curTickerBuyDate)
		checkTickerBuy = execute(cur, conn, data, checkTickerBuyQuery)
		checkTickerBuy = checkTickerBuy.fetchall()
		print("Tested: " + randomTicker + "and found it passed: " + checkTickerBuy) '''
		while(canBuyTicker == False):
			#print("Bad seed, repicking")
			randomTicker = random.choice(list(tickerDict.keys()))
			randomTicker = re.sub('[^A-Za-z0-9]+', '', randomTicker)
			#print(randomTicker)
			data = (randomTicker, curTickerBuyDate)
			selectTickerSatisfying = execute(cur, conn, data, selectTickerSatisfyingQuery)
			selectTickerSatisfying = selectTickerSatisfying.fetchall()
			canBuyTicker = (len(selectTickerSatisfying) > 0)
		#print("settled on randomTicker = " + randomTicker)
		curTickerSellDate = sellDate
		curTickerBuyPriceQuery = "SELECT open_price FROM stock_prices WHERE ticker = %s AND pdate = %s"
		data = (randomTicker, curTickerBuyDate)
		buyPrice = execute(cur, conn, data, curTickerBuyPriceQuery)
		buyPrice = buyPrice.fetchall()[0][0]
		#print(buyPrice)
		#print("buyPrice is: " + buyPrice)
		curTickerSellPriceQuery = "SELECT open_price FROM stock_prices WHERE ticker = %s and pdate = %s"
		data = (randomTicker, curTickerSellDate)
		sellPrice = execute(cur, conn, data, curTickerSellPriceQuery)
		sellPrice = sellPrice.fetchall()[0][0]
		#print("sellPrice is: " + sellPrice)
		if((budget - sellPrice) <= 0):
			canBuyMoreStocks = False
		else:
			budget = budget - sellPrice
			if(randomTicker in portfolioDict.keys()):
				portfolioDict[randomTicker][4] += 1
			else:
				portfolioDict[randomTicker] = [curTickerBuyDate, curTickerSellDate, float(buyPrice), float(sellPrice), 1]
		#print(budget)
	return portfolioDict

'''
def main():
	fileLocation = "../uploads/flatland.txt"
	tickerTrie = trieMaker.query_database_for_tickers()
	print(tickerTrie)
	portfolioDict = textPortfolio.parse_text(fileLocation, tickerTrie)
	print(portfolioDict)
	portfolio = make_portfolio(portfolioDict, 1000, "2007-02-16", "2016-02-16")
	print(portfolio)

main() '''
