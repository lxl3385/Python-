# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains=['github.com']

    @property
    def start_urls (self):
        url_tmpl= 'https://github.com/shiyanlou?page{}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for repository in response.css('li.public'):
            item= RepositoryItem({
                'name':repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)"),
                'update_time':repository.xpath('.//relative-time/@datetime').extract_first()
            })
            yield item

#'name':course.css('a::text').re_first("\n\s*(.*)"),
#'update_time':course.css('relative-time::attr(datetime)').extract_first()
