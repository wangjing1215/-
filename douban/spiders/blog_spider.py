import scrapy
import re
from ..items import DOUItem
from scrapy.http import Request
import time
import time as q
# -*- coding: utf-8 -*-
class Spider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["http://www.douban.com"]
    start_urls = ['https://movie.douban.com/subject/24773958/comments?status=P', 'https://movie.douban.com/subject/24773958/comments?start=0&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=20&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=40&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=60&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=80&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=100&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=120&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=140&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=160&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=180&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=200&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=220&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=240&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=260&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=280&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=300&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=320&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=340&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=360&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=380&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=400&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=420&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=440&limit=20&sort=new_score&status=P', 'https://movie.douban.com/subject/24773958/comments?start=460&limit=20&sort=new_score&status=P',]

    def parse(self, response):
        #print(response.body)
        print('*********************************')
        print(response.url, response)

        print('*********************************')
        thehtml = str(response.body_as_unicode())
        #print(thehtml)
        starl = ["很差", "较差", "还行", "推荐", "力荐"]
        dou = DOUItem()
        usernamelist = re.findall('<a title="(.*)" href="https://www.douban.com', thehtml)
        votelist = re.findall('<span class="votes">(.*)</span>', thehtml)
        starlist = re.findall('rating" title="(.*)"></span>', thehtml)
        datalist = re.findall('<span class="comment-time " title="(.*)">', thehtml)
        commentlist = re.findall('<span class="short">(.*)</span>', thehtml)
        #print(usernamelist,votelist,starlist,datalist,commentlist)
        for username,vote,star,data,comment in zip(usernamelist,votelist,starlist,datalist,commentlist):
            dou['username'] = username
            dou['vote'] = vote
            dou['star'] = starl.index(star)+1
            dou['data'] = data
            dou['comment'] = comment
            yield dou
