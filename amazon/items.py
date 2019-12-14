# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AmazonItem(scrapy.Item):
    page_title = scrapy.Field()
    book_title = scrapy.Field()
    book_author = scrapy.Field()
    book_price = scrapy.Field()
    book_image_link = scrapy.Field()
    book_detail_link = scrapy.Field()
