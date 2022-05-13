import scrapy


class OtzovikSpider(scrapy.Spider):
    name = 'otzovik'
    allowed_domains = ['otzovik.com']
    start_urls = ['http://otzovik.com/']

    def parse(self, response):
        pass
