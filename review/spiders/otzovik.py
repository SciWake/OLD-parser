import os
import pickle
import scrapy
import csv
from review.items import ReviewItem
from scrapy.loader import ItemLoader


class OtzovikSpider(scrapy.Spider):
    name = 'otzovik'
    allowed_domains = ['otzovik.com']
    start_urls = ['https://otzovik.com/health/fragrance']

    with open(os.path.join(os.getcwd(), 'database.csv'), 'r', newline='', encoding='UTF-8') as csv_file:
        id_to_csv = [row['id'] for row in csv.DictReader(csv_file)]

    def start_requests(self):
        with open(os.path.join(os.getcwd(), 'cookies.pickle'), 'rb') as f:
            cookies = pickle.load(f)

        yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies=cookies)

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
            if 'https://otzovik.com' + review_url.extract() in self.id_to_csv:  # Повторный обход
                continue
            yield response.follow(review_url, callback=self.parse_review)

    def parse_review(self, response):
        item = ItemLoader(ReviewItem(), response)
        item.add_value('id', response.url)
        item.add_css('title', 'div.product-header a.product-name span::text')
        item.add_css('rating', 'table.product-props abbr.rating::attr("title")')
        item.add_css('recommend_to_friend', 'table.product-props td.recommend-ratio::text')
        item.add_css('overall_impression', 'table.product-props i.summary::text')
        item.add_css('product_rating_details', 'div.review-contents div.product-rating-details div::attr("title")')
        item.add_css('review_count_likes', 'div.review-bar span.review-btn::text')
        item.add_css('review_count_comments', 'div.review-bar a.review-comments::text')
        item.add_css('dignities', 'div.review-contents div.review-plus::text')
        item.add_css('disadvantages', 'div.review-contents div.review-minus::text')
        item.add_css('review_text', 'div.review-contents div.review-body::text')

        item.add_css('user_login', 'div.review-header div.login-col span::text')
        item.add_css('user_karma', 'div.review-header div.karma-col div.karma::text')
        item.add_css('reviews_count', 'div.review-header div.reviews-col a.reviews-counter::text')
        yield item.load_item()
