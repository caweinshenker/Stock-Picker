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
		dates = []
		opens = []
		closes = []
		for row in self.data:
			dates.append(row[1])
			opens.append(row[2])
			closes.append(row[3])
		plt.rcParams.update({'font.size': 10})
		plt.title('Open/Close Prices')
		plt.plot(dates, opens, 'r-', dates, closes, 'b-')
		plt.xlabel('Date')
		plt.ylabel('Price (USD)')
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


class Volume_Graph(Open_Close_Graph):
	
	def make_graph(self):
		print("here!")
		dates = []
		volumes = []
		for row in self.data:
			dates.append(row[0])
			volumes.append(row[1])
		plt.rcParams.update({'font.size': 10})
		plt.title('Trade Volume')
		plt.plot(dates, volumes, 'gs', markersize=2)
		plt.xlabel('Date')
		plt.ylabel('Volume')
		fig = plt.gcf()
		self.img = StringIO.StringIO()
		fig.savefig(self.img)
		self.img.seek(0)
		plt.close()

