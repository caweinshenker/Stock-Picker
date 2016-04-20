from nytimesarticle import articleAPI


class NYT_Parser:
	
	def __init__(self):
		self.api = articleAPI("9ed601a914bd7b99e85df32fcb1b1a8b:9:75048351")
		self.news = []

	def find_articles(self, company, date):
		'''
		Accept a year in 'YYYY-MM-DD' format and a search query and return a list of parsed articles in dictionaries
		'''
		date = int("".join(date.split("-")))
		print(company)
		print(date)
		articles = self.api.search(q = company, fq = {'source':['Reuters', 'AP', 'The New York Times']}, begin_date = date, sort = 'oldest')
		self.__parse_articles(articles)

	def __parse_articles(self, articles):
		'''
		Take in an NYT api response and parse articles into dictionary list
		'''
		for article in articles['response']['docs']:
			dic = {}
			dic['id'] = article['_id']
			if article['abstract'] is not None:
				dic['abstract'] = article['abstract'].encode("utf8")
			dic['headline'] = article['headline']['main'].encode("utf8")
			dic['desk'] = article['news_desk']
			dic['date'] = article['pub_date'][0:10]
			dic['section'] = article['section_name']
			if article['snippet'] is not None:
				dic['snippet'] = article['snippet'].encode("utf8")
			dic['source'] = article['source']
			dic['type'] = article['type_of_material']
			dic['url'] = article['web_url']
			dic['word_count'] = article['word_count']
			self.news.append(dic) 	


	def get_news(self):
		'''
		Return the parsed articles
		'''
		return self.news
				
