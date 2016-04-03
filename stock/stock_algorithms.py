class Stock_Algorithms:
  # will need to convert these all to psycopg commands

  def priceGraphDataBetween(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, return a list of date x-values
    # and a list of price y-values for that stock ticker. To be used for graphing with matplotlib

    xList = []
    yList = []

    return (xList, yList)

  def dividendGraphDataBetween(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, return a list of date x-values
    # and a list of dividend y-values for that stock ticker. To be used for graphing with matplotlib

    xList = []
    yList = []

    return (xList, yList)

  def priceHighBetween(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, return the maximum
    # price of that stock over the startDate-endDate period.

    maxPrice = 0
    maxPrice = "select max(close_price) from stock_price where ticker = ticker AND date >= startDate AND date <= endDate"
    return maxPrice

  def dividendHighBetween(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, return the maximum
    # dividend return of that stock over the startDate-endDate period.

    maxDividend = 0
    maxDividend = "select max(price) from stock_dividend where ticker = ticker AND date >= startDate AND date <= endDate"
    return maxDividend

  def priceLowBetween(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, return the minimum
    # price of that stock over the startDate-endDate period.

    minPrice = 0
    minPrice = "select min(close_price) from stock_price where ticker = ticker AND date >= startDate AND date <= endDate"
    return minPrice

  def dividendLowBetween(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, return the minimum
    # dividend return of that stock over the startDate-endDate period.

    minDividend = 0
    minDividend = "select min(price) from stock_dividend where ticker = ticker AND date >= startDate AND date <= endDate"
    return minDividend

  def priceGrowthOverTimeFrom(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, returns a tuple containing the net price change
    # and percentage price change of a stock.
    
    startDatePrice = "select close_price from stock_price where ticker = ticker AND pdate = startDate"
    startDatePrice *= quantity
    endDatePrice = "select close_price from stock_price where ticker = ticker AND pdate = endDate"
    endDatePrice *= quantity
    return (endDatePrice - startDatePrice, (endDatePrice - startDatePrice) / startDatePrice)

  
  def dividendOverTimeFrom(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity, startDate, and endDate, returns the dividend returns
    # from startDate to endDate

    dividendTotal = 0 # default value in case stock has no dividends
    dividendTotal += "select sum(ex_date) from stock_dividend where date >= startDate AND date <= endDate"
    dividendTotal *= quantity
    return dividendTotal

  def reinvestOverTimeFrom(self, ticker, quantity, startDate, endDate):
    # for a stock ticker, given a quantity purchased, startDate, and endDate, returns a tuple 
    # containing the net price change and percentage price change of a stock under the
    # assumption that all dividend earnings are reinvested when possible
    
    startDatePrice = "select close_price from stock_price where ticker = ticker AND pdate = startDate"
    startDatePrice *= quantity
    return 0





  
