from datetime import date, timedelta as td

'''Handle manipulation of date strings to conform with postgresql requirements'''

class Date_Parser:
	
	def __init__(self, start_date, end_date):
		self.start_date = start_date
		self.end_date = end_date
		self.start = None
		self.end = None
		self.date_range = []
		self.__create_datetimes()
		self.__create_date_range()

	def __create_datetimes(self):
		start_split = self.start_date.split("-")
		end_split = self.end_date.split("-")
		self.start =  date(int(start_split[0]), int(start_split[1]), int(start_split[2]))
		self.end = date(int(end_split[0]), int(end_split[1]), int(end_split[2]))

	
	def __create_date_range(self):
		delta = self.end - self.start
		for i in range(delta.days + 1):
			self.date_range.append(str(self.start + td(days =i)))

	def get_date_range(self):
		return self.date_range
		
	


