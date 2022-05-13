# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def get_details(values):
    print(1)


class ReviewItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    recommend_to_friend = scrapy.Field(output_processor=TakeFirst())
    overall_impression = scrapy.Field(output_processor=TakeFirst())
    product_rating_details = scrapy.Field(input_processor=Compose(get_details))
    review_likes = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    review_comments = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    dignities = scrapy.Field(output_processor=TakeFirst())
    disadvantages = scrapy.Field(output_processor=TakeFirst())
    review_text = scrapy.Field(input_processor=Compose(get_details))
