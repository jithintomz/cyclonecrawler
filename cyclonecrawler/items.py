# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CyclonecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    identifier = scrapy.Field()
    name = scrapy.Field()
    forecast_time = scrapy.Field()
    forecasts = scrapy.Field()
    history = scrapy.Field()
