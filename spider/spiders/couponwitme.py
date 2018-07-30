# -*- coding: utf-8 -*-
import scrapy

class CouponwitmeSpider(scrapy.Spider):
    name="couponwitme"
    allow_domains=["couponwitme.com"]

    def start_requests(self):
        # for item in range(65, 91):
        #     url = "https://www.couponwitme.com/stores/"+ chr(item) + "/"
        #     yield scrapy.Request(url=url, callback=self.parse)

        url = "https://www.couponwitme.com/stores/Other/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 爬虫分发

        # 直接到内容页
        for page in response.xpath('//*[@class="all_stores"]/ul[@class="storeslist"]/li/a/@href').extract():
            # print(page)
            yield response.follow(page, self.parse_term)

        # 类别页
        for page in response.xpath('//*[@id="left"]/ul[@id="category"]/li/a/@href').extract():
            # print(page)
            yield response.follow(page, self.parse_category)

    def parse_term(self, response):

        #coupon list
        coupon_list = []
        for coupon_block in response.xpath('//*[@id="coupon_list"]//div[contains(@class, "coupon_block")]'):
            coupon = {
                'id': coupon_block.xpath('//a[contains(@id, "divcover_")]/@id').extract_first().split("_")[1],
                'title': coupon_block.xpath('//p[contains(@class, "coupon_title")]/a/text()').extract_first(),
                'description': coupon_block.xpath('//span[contains(@class, "cpdesc")]/text()').extract_first(),
                'restriction': coupon_block.xpath('//span[contains(@class, "coupon_restriction")]/text()').extract_first(),
                'code': coupon_block.xpath('//span[contains(@class, "coupon_code")]/text()').extract_first(),
                'dst_url': coupon_block.xpath('//a[contains(@id, "divcover_")]/@href').extract_first(),
                'expire_time': coupon_block.xpath('//div[contains(@class, "coupon_infor")]/p[last()]/text()').extract_first(),
                'click_count': coupon_block.xpath('//*[contains(@class, "click")]/text()').extract_first(),
            }
            coupon_list.append(coupon)

        # data
        yield {
            'h1': response.xpath('//h1/text()').extract_first(),
            'dst_url': response.xpath('//*[@id="store_screen"]/a/@href').extract_first(),
            'img': response.xpath('//*[@id="store_screen"]/a/img/@src').extract_first(),
            'coupon_list': coupon_list
        }

    def parse_category(self, response):
        # print(response.url)
        pass