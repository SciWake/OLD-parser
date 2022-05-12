import scrapy


class IrecommendSpider(scrapy.Spider):
    name = 'irecommend'
    allowed_domains = ['irecommend.ru']
    start_urls = ['http://irecommend.ru/']

    def parse(self, response):
        pass
