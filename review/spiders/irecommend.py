import scrapy


class IrecommendSpider(scrapy.Spider):
    name = 'irecommend'
    allowed_domains = ['irecommend.ru']
    start_urls = ['https://irecommend.ru/catalog/list/31']

    def parse(self, response):
        # Getting pagination links
        print()
        for page_url in response.css('div.item-list ul.pager li.pager-item a::attr("href")'):
            yield response.follow(page_url, callback=self.parse)

        # Getting links to product
        for product_url in response.css('div.view-content div.ProductTizer a.reviewsLink::attr("href")'):
            yield response.follow(product_url, callback=self.parse_product)

    def parse_product(self, response):
        for prod_page_url in response.css('div.item-list ul.pager li a::attr("href")'):
            yield response.follow(prod_page_url, callback=self.parse_product)

        # Getting links to review
        for review_url in response.css('div.item-list ul.list-comments li.item div.reviewTitle a::attr("href")'):
            yield response.follow(review_url, callback=self.parse_product)

    def parse_review(self, reponse):
        pass
