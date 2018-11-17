# -*- coding: utf-8 -*-
import pymysql
import  time
class douPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='172.18.0.2', user='root', passwd='123456', db='scrapy', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "SELECT * FROM douban_3 WHERE username = '{}'".format(item['username'])
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        star = 0
        for row in results:
            name = row[1]
            star = row[3]
        if int(star) == int(item['star']) and str(name) == str(item['username']):
            print("该条记录已存在0---------------------------------------------")
        else:
            print('新记录+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            insert_sql = "INSERT INTO douban_3(username,vote,star,date,comment) VALUES('{}', '{}', '{}'," \
                         " '{}','{}')".format(item['username'], item['vote'], item['star'], item['data'],
                                              item['comment'])
            self.cursor.execute(insert_sql)
            self.conn.commit()
        return item

    def spider_close(self, spider):
        self.conn.close()