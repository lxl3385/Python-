# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
 


class RepositoryItem(scrapy.Item):
    name=scrapy.Field()
    update_time=scrapy.Field()
