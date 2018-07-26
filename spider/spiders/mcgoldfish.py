# -*- coding: utf-8 -*-
import scrapy

# 分页爬取
class McgoldfishSpider(scrapy.Spider):
    name = 'mcgoldfish'
    allowed_domains = ['mcgoldfish.com']
    start_urls = ['https://www.mcgoldfish.com/']

    def parse(self, response):
        print(response.body)
        nextPage = response.xpath('//div[@id="content"]//ul[contains(@class, "pagination")]/li[last()]/a/@href').extract_first()

        if nextPage is not None:
            print('继续执行: '+ nextPage)
            yield response.follow(nextPage, callback=self.parse)


