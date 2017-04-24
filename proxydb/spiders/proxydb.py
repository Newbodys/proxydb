import scrapy
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.proxydb

class proxydb(scrapy.Spider):
	name = "proxydb"
	start_urls = ['http://proxydb.net/?protocol=http&anonlvl=4&country=CN&availability=75&offset=0']

	def parse(self,response):

		proxy_num_str = response.xpath('//small[@class="text-muted"]/text()').re(r'[1-9]\d*')
		proxy_num = int(proxy_num_str[0])

		for num in xrange(0,proxy_num,50):
			proxy_url = 'http://proxydb.net/?protocol=http&anonlvl=4&country=CN&availability=75&offset='+str(num)
			yield scrapy.Request(url=proxy_url,callback=self.parse_page)

	def parse_page(self,response):
		proxy_add = response.xpath('//tbody/tr/td/a/text()').extract()

		for address in proxy_add:
			ip_count = db.address.count()
			if db.address.find_one({"address_ip":address})==None:
				ip_count = db.address.count()
				db.address.insert({'address_ip':address,'ip_index':(ip_count+1)})
