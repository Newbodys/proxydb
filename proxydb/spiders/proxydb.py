import scrapy
import math
from pymongo import MongoClient

class proxydb(scrapy.Spider):
	name = "proxydb"
	start_urls = ['http://proxydb.net/?anonlvl=4&country=CN&offset=0']

	def parse(self,response):

		proxy_num_str = response.xpath('//small[@class="text-muted"]/text()').re(r'[1-9]\d*')
		proxy_num = int(proxy_num_str[0])

		for num in xrange(0,proxy_num,50):
			proxy_url = 'http://proxydb.net/?anonlvl=4&country=CN&offset='+str(num)
			yield scrapy.Request(url=proxy_url,callback=self.parse_page)

	def parse_page(self,response):
		proxy_add = response.xpath('//tbody/tr/td/a/text()').extract()
		
		client = MongoClient('localhost',27017)
		db = client.proxy
		db.address.insert({'proxy_add':proxy_add})
		print "add"
