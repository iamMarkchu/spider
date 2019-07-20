# -*- coding: utf-8 -*-
# import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


# class SpiderPipeline(object):
#
#     def __init__(self, mongo_uri, mongo_db, mongo_user, mongo_password):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#         self.mongo_user = mongo_user
#         self.mongo_password = mongo_password
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
#             mongo_user=crawler.settings.get('MONGO_USER'),
#             mongo_password=crawler.settings.get('MONGO_PASSWORD'),
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri, username=self.mongo_user, password=self.mongo_password)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         # 使用spider的名字作为 collection名字
#         collection_name = spider.name
#         self.db[collection_name].insert_one(dict(item))
#         return item


class MzituImagePipeline(ImagesPipeline):
    referer = 'https://www.mzitu.com'

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename = '%s/%s.jpg' % (item['tid'], item['order'])
        return filename



    def get_media_requests(self, item, info):
        urls = [item['img_url']]
        r = [Request(x, headers={"referer": "https://www.mzitu.com/"}, meta={"item": item}) for x in urls]
        print(r)
        return r

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
