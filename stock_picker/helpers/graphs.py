import matplotlib.pyplot as plt, mpld3
import matplotlib.patches as mpatches
import StringIO
import psycopg2
import psycopg2.extras
import datetime

class Open_Close_Graph:

	"""
	Create a graph of a stock's open and close prices
	"""
	
	def __init__(self, ticker = None, data = None):
		self.ticker = ticker
		self.data = data
		self.img = None

	def make_graph(self):
		prices = [dict(ticker = row[0], pdate = row[1], open_price = row[2], close = row[3]) for row in self.data]
		dates = []
		opens = []
		closes = []
		for day in prices:
			dates.append(day["pdate"])
			opens.append(day["open_price"])
			closes.append(day["close"])
		plt.rcParams.update({'font.size': 12})
		plt.plot(dates, opens, 'r-', dates, closes, 'b-')
		plt.xlabel('Date')
		plt.ylabel('Price')
		red_patch = mpatches.Patch(color = 'red', label = 'Open price')
		blue_patch = mpatches.Patch(color = 'blue', label = 'Close price')
		plt.legend(handles=[red_patch, blue_patch])
		fig = plt.gcf()
		self.img = StringIO.StringIO()
		fig.savefig(self.img)
		self.img.seek(0)
		plt.close()

	def get_fig(self):
		if self.img != None:
			self.img.seek(0)
			return self.img
		else:
			return None

