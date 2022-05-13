# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def get_details(values):
    data = {}
    for val in values:
        keys = val.split()
        data[keys[0].replace(':', '')] = int(values[0].split()[1])
    return data


def join_text(text):
    return ' '.join(text)


class ReviewItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    recommend_to_friend = scrapy.Field(output_processor=TakeFirst())
    overall_impression = scrapy.Field(output_processor=TakeFirst())
    product_rating_details = scrapy.Field(input_processor=Compose(get_details), output_processor=TakeFirst())
    review_count_likes = scrapy.Field(input_processor=MapCompose(lambda x: int(x)), output_processor=TakeFirst())
    review_count_comments = scrapy.Field(input_processor=MapCompose(lambda x: int(x)), output_processor=TakeFirst())
    dignities = scrapy.Field(output_processor=TakeFirst())
    disadvantages = scrapy.Field(output_processor=TakeFirst())
    review_text = scrapy.Field(input_processor=Compose(join_text), output_processor=TakeFirst())

    user_login = scrapy.Field(output_processor=TakeFirst())
    user_karma = scrapy.Field(input_processor=MapCompose(lambda x: int(x)), output_processor=TakeFirst())
    reviews_count = scrapy.Field(input_processor=MapCompose(lambda x: int(x)), output_processor=TakeFirst())
