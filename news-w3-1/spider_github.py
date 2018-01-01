# _*_ coding:utf-8 _*_
import scrapy

class SpiderGithub(scrapy.Spider):
    name='github-courses'
    
    @property
    def start_urls(self):
    	#url_tmpl='https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self,response):
        for course in response.css('li.py-4'):
            yield{
                'name':course.css('a::text').re_first("\n\s*(.*)"),
                'update_time':course.css('relative-time::attr(datetime)').extract_first()
            }
