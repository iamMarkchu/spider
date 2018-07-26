# -*- coding: utf-8 -*-
import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        # 获取内容
        movieList = response.xpath('//*[@id="content"]//ol[contains(@class, "grid_view")]/li/div[contains(@class, "item")]')

        for movie in movieList:
            yield {
                'title': movie.xpath('//div[contains(@class, "info")]/div[contains(@class, "hd")]/a/span[@class="title"][1]/text()').extract_first(),
                'img': movie.xpath('//div[@class="pic"]/a/img/@src').extract_first()
            }

        # 下一页逻辑
        nextPage = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract_first()
        if nextPage is not None:
            print(nextPage)
            yield response.follow(nextPage, callback=self.parse)
