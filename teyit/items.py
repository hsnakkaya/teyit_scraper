# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    claim = scrapy.Field()
    verdict = scrapy.Field()
    is_claim = scrapy.Field()
    link_list = scrapy.Field()
    img_link_list = scrapy.Field()
    text_all = scrapy.Field()
    tags = scrapy.Field()

    pass
