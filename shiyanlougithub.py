# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import CourseItem


class ShiyanlougithubSpider(scrapy.Spider):
    name = 'shiyanlougithub'
    @property
    def start_urls(self):
        url_tmpl="https://github.com/shiyanlou?page={}&tab=repositories"
        return (url_tmpl.format(i) for i in range(1,5))
    def parse(self,response):
        for course in response.css('li.col-12'):
            item=CourseItem({
                'name':course.xpath('.//h3/a/text()').re_first('(\S+)'),
                'update_time':course.xpath('.//relative-time/@datetime').extract_first()
            })
            course_url = response.urljoin(course.xpath('.//h3/a/@href').extract_first())
            request = scrapy.Request(course_url,callback=self.detail_parse)
            request.meta['item']=item
            yield request
    def detail_parse(self,response):
        item=response.meta['item']
        item['commits']=response.xpath('//span[@class="num text-emphasized"]/text()').extract()[0].strip()
        item['branches']=response.xpath('//span[@class="num text-emphasized"]/text()').extract()[1].strip()
        item['releases']=response.xpath('//span[@class="num text-emphasized"]/text()').extract()[2].strip()
        yield item
