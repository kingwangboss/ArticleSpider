# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self):
        self.file.closed


class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'kingwangboss', 'article_spride', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(url_object_id, title, url, fav_nums,content,tags,create_date,praise_nums)
            VALUES (%s,%s, %s, %s, %s,(%s),(%s),(%s))
        """
        self.cursor.execute(insert_sql, (item["url_object_id"],item["title"],
                                         item["url"], item["fav_nums"],item["content"],
                                         item["tags"],item["create_date"],item["praise_nums"]))

        self.conn.commit()

class MysqltwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
                    insert into article(url_object_id, title, url, fav_nums,content,tags,create_date,praise_nums)
                    VALUES (%s,%s, %s, %s, %s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (item["url_object_id"], item["title"],
                                         item["url"], item["fav_nums"], item["content"],
                                         item["tags"], item["create_date"], item["praise_nums"]))

class JsonExporterPipeline(object):
    #调用scrapy提供的jsonexporter导出json文件
    def __init__(self):
        self.file = open('articleexporter.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
                item["front_image_path"] = image_file_path
        return item