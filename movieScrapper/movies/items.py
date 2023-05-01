# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    year=scrapy.Field()
    title=scrapy.Field()
    rating=scrapy.Field()
    no_of_reviews=scrapy.Field()
    genres=scrapy.Field()
    runtime=scrapy.Field()
    gross=scrapy.Field()