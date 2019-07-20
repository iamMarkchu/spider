# -*- coding: utf-8 -*-
import scrapy

from spider.items import MzituItem


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['https://www.mzitu.com/']
    root_url = 'https://www.mzitu.com'

    def parse(self, response):
        for url in response.xpath('//*[contains(@class, "postlist")]/ul/li/a/@href').extract():
            yield response.follow(url, self.parse_detail)

        for url in response.xpath('//*[contains(@class, "nav-links")]/a/@href').extract():
            yield response.follow(url, self.parse)

    def parse_detail(self, response):
        is_default_page = not (len(response.url.split('/')) > 4)
        if is_default_page:
            last_page = response.xpath('//*[contains(@class, "pagenavi")]/a[last()-1]/span/text()').extract_first()
            for index in range(2, int(last_page)):
                yield response.follow(response.url + "/" + str(index), self.parse_detail)
        item = MzituItem()
        item['tid'] = response.url.split('/')[3]
        item['order'] = response.url.split('/')[4] if not is_default_page else '1'
        item['img_url'] = response.xpath('//*[contains(@class, "main-image")]/p/a/img/@src').extract_first()
        item['title'] = response.xpath('//h2[contains(@class, "main-title")]/text()').extract_first()
        item['time'] = response.xpath('//*[contains(@class, "main-meta")]/span[2]/text()').extract_first()
        item['category'] = response.xpath('//*[contains(@class, "main-meta")]/span[1]/a/text()').extract_first()
        item['tags'] = ','.join(response.xpath('//*[contains(@class, "main-tags")]/a/text()').extract())
        yield item
