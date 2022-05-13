import scrapy
from review.items import ReviewItem
from scrapy.loader import ItemLoader
from time import time


class OtzovikSpider(scrapy.Spider):
    name = 'otzovik'
    allowed_domains = ['otzovik.com']
    start_urls = ['https://otzovik.com/health/fragrance']
    cookies = [{'domain': '.otzovik.com', 'expiry': 1683959077, 'httpOnly': False, 'name': 'refreg', 'path': '/',
                'secure': True,
                'value': '1652423077~https%3A%2F%2Fotzovik.com%2Fhealth%2Ffragrance%2F%3F%26capt4a%3D4571652423066491'},
               {'domain': '.otzovik.com', 'expiry': 1683959077, 'httpOnly': False, 'name': '_ym_d', 'path': '/',
                'secure': True, 'value': '1652423078'},
               {'domain': '.otzovik.com', 'expiry': 1683959077, 'httpOnly': False, 'name': '_ym_uid', 'path': '/',
                'secure': True, 'value': '1652423078586409043'},
               {'domain': '.otzovik.com', 'expiry': 1652495077, 'httpOnly': False, 'name': '_ym_isad', 'path': '/',
                'secure': True, 'value': '2'},
               {'domain': '.otzovik.com', 'httpOnly': True, 'name': 'ROBINBOBIN', 'path': '/', 'secure': True,
                'value': '7afc807c9bc158516e3ccff5aa'},
               {'domain': '.otzovik.com', 'expiry': 1715581855, 'httpOnly': True, 'name': 'ssid', 'path': '/',
                'secure': False, 'value': '3594085729'}]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=self.cookies  # переносить cookies для запроса
            # headers = headers
        )

    def parse(self, response):
        # Getting base pagination links
        for page_url in response.css('div.pager a.nth::attr("href")'):
            yield response.follow(page_url, callback=self.parse)

        # Getting links to product
        for product_url in response.css('div.product-list tr a.product-name::attr("href")'):
            yield response.follow(product_url, callback=self.parse_product)

    def parse_product(self, response):
        # Getting product pagination links
        for prod_page_url in response.css('div.pager a.nth::attr("href")'):
            yield response.follow(prod_page_url, callback=self.parse_product)

        # Getting links to review
        for review_url in response.css('div.review-list-chunk div.mshow0 a.review-read-link::attr("href")'):
            yield response.follow(review_url, callback=self.parse_review)

    def parse_review(self, response):
        item = ItemLoader(ReviewItem(), response)
        data = {
            'title': response.css('div.product-header a.product-name span::text')[0].extract(),

        }
        item.add_value('id', response.url)
        item.add_css('title', 'div.product-header a.product-name span::text')
        item.add_css('rating', 'table.product-props abbr.rating::attr("title")')
        item.add_css('recommend_to_friend', 'table.product-props td.recommend-ratio::text')
        item.add_css('overall_impression', 'table.product-props i.summary::text')
        item.add_css('product_rating_details', 'div.review-contents div.product-rating-details div::attr("title")')
        item.add_css('review_likes', 'div.review-bar span.review-btn::text')
        item.add_css('review_comments', 'div.review-bar span.review-comments')
        item.add_css('dignities', 'div.review-contents div.review-plus::text')
        item.add_css('disadvantages', 'div.review-contents div.review-minus::text')
        item.add_css('review_text', 'iv.review-contents div.review-body::text')
        yield item.load_item()
