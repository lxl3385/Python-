# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    @property
    def start_urls (self):
        url_tmpl= 'https://github.com/shiyanlou?tab=repositories&page{}'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for course in response.css('li.py-4'):
            yield RepositoryItem({
                'name':course.css('a::text').re_first("\n\s*(.*)"),
                'update_time':course.css('relative-time::attr(datetime)').extract_first()
            })
