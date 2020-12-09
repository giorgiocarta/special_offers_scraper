# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoppingItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field()
    listing = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    tracking = scrapy.Field()
    tracking_type = scrapy.Field()
    raw_week = scrapy.Field()
    iso_week = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    crawl_date = scrapy.Field()
    week_number = scrapy.Field()
    pk = scrapy.Field()
