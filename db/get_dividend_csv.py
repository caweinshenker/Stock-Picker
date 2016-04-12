import sys
import csv
import urllib.request
import requests
from time import sleep


#Stocks files
stock_files   = ["nasdaq.csv", "amex.csv", "nyse.csv"]

def get_ticker_list():
	"""Open the available lists of stocks, extract their tickers, and call scrape_dividend_to_csv

	Params: cursor (database cursor)
	Returns: ticker_list (list of stock tickers)
	"""
	for stock_file in stock_files:
		ticker_list = []
		names_list = []
		with open(stock_file, 'r') as csvfile:
			firstline = True
			reader = csv.reader(csvfile, delimiter =",")
			for row in reader:
				if firstline:
					firstline = False
					continue
				ticker_list.append(row[0])
				names_list.append(row[1])
	return(ticker_list)

def scrape_dividend_to_csv(ticker_list):
  ''' For each stock, get the dividend information from 1990 until 2016 and store it in a csv file called dividend_info.csv '''
  ticker_list = get_ticker_list()
  with open("dividend_info.csv", "w") as dividendFile:
    for ticker in ticker_list:
      tickerQuery = ticker.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          ".":  r"\."}))

      urlString = "http://ichart.finance.yahoo.com/table.csv?s=" + tickerQuery + "&a=9&b=26&c=1990&d=9&e=25&f=2016&g=v&ignore=.csv"
      try: 
        dataObject = urllib.request.urlopen(urlString)
      except Exception as e:
        continue
      dataReader = csv.reader(dataObject.read().decode('utf-8'), delimiter='\t')
      r = requests.get(urlString, verify=False)
      text = r.text
      reader = csv.reader(text.splitlines(), delimiter=',')
      dividendFile.write(ticker)
      dividendFile.write(r.text)
      dividendFile.write("end_of_data")

      sleep(5)
     
def main():
  scrape_dividend_to_csv(get_ticker_list)

main()


