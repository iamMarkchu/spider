# -*- coding: utf-8 -*-
import scrapy

class CouponwitmeSpider(scrapy.Spider):
    name="couponwitme"
    allow_domains=["couponwitme.com"]
    root_url = "https://www.couponwitme.com"

    def start_requests(self):
        urls = []
        for item in range(97, 122):
            url = self.root_url + "/stores/"+ chr(item) + "/"
            urls.append(url)
        urls.append(self.root_url + "/stores/other/")

        # store页面列表
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        # 类别页面列表
        url = self.root_url + "/category/"
        yield scrapy.Request(url=url, callback=self.parse_all_category)

    def parse(self, response):
        # 爬虫分发
        for url in response.xpath('//*[@class="letter"]/ul/li/a/@href').extract():
            yield response.follow(url, self.parse_term)

    def parse_term(self, response):
        #coupon list
        coupon_list = []
        for coupon_block in response.xpath('//ul[contains(@class, "c_list")]/li'):
            coupon = {
                'id': coupon_block.xpath('./@data-id').extract_first(),
                'title': coupon_block.xpath('.//p[contains(@class, "c_title")]/a/text()').extract_first(),
                'description': coupon_block.xpath('.//div[contains(@class, "des")]/text()').extract_first(),
                'code': coupon_block.xpath('.//div[contains(@class, "show_code")]/a/code/text()').extract_first(),
                'dst_url': coupon_block.xpath('.//div[contains(@class, "show_code")]/a/@href').extract_first(),
                'promo_detail': ' '.join(coupon_block.xpath('.//div[contains(@class, "promo_infor_center")]/span/text()').extract())
            }
            coupon_list.append(coupon)

        # term data
        yield {
            'h1': response.xpath('//h1/text()').extract_first(),
            'name': response.xpath('//div[contains(@class, "shop-at-link-container")]/a/@title').extract_first(),
            'dst_url': response.xpath('//*[@class="term_info"]/a/@href').extract_first(),
            'request_path': response.url.replace(self.root_url, ""),
            'img': response.xpath('//*[@class="term_info"]/a/img/@src').extract_first(),
            'categories': '->'.join(response.xpath('//*[contains(@class,"breadcrumbs")]/a/text()').extract()[1:]),
            'desc': response.xpath('//*[contains(@class, "store_de")]').extract_first(),
            'coupon_list': coupon_list
        }

        # 获取 Related Stores Popular Stores链接
        for url in response.xpath('//*[contains(@class, "newstore_list")]/a/@href').extract():
            yield response.follow(url, self.parse_term)

        # 获取category页面
        for url in response.xpath("//div[contains(@class, 'cate_list')]/a/@href").extract():
            yield response.follow(url, self.parse_category)

    def parse_category(self, response):
        for url in response.xpath("//*[contains(@class, 'storelist')]/ul/li/a/@href").extract():
            yield response.follow(url, self.parse_term)

    def parse_all_category(self, response):
        for category_block in response.xpath('//*[contains(@class, "letter")]/ul').extract():
            yield response.follow(category_block.xpath('.//div[contains(@class, "one_letter")]/a/@href'), self.parse_category)
            for url in category_block.xpath('.//li/a/@href').extract():
                yield response.follow(url, self.parse_category)