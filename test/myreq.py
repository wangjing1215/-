# -*- coding: utf-8 -*-
import requests as req
import time
import re
from requests.cookies import RequestsCookieJar
import pymysql
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

start_urls = [
              'https://movie.douban.com/subject/24773958/comments?start=420&limit=20&sort=new_score&status=P',
              'https://movie.douban.com/subject/24773958/comments?start=440&limit=20&sort=new_score&status=P',
              'https://movie.douban.com/subject/24773958/comments?start=460&limit=20&sort=new_score&status=P', ]

def parse(response):
    # print(response.body)
    print('*********************************')
    thehtml = str(response)
    # print(thehtml)
    starl = ["很差", "较差", "还行", "推荐", "力荐"]
    usernamelist = re.findall('<a title="(.*)" href="https://www.douban.com', thehtml)
    votelist = re.findall('<span class="votes">(.*)</span>', thehtml)
    starlist = re.findall('rating" title="(.*)"></span>', thehtml)
    datalist = re.findall('<span class="comment-time " title="(.*)">', thehtml)
    commentlist = re.findall('<span class="short">(.*)</span>', thehtml)
    #print(usernamelist,votelist,starlist,datalist,commentlist)
    for username, vote, star, data, comment in zip(usernamelist, votelist, starlist, datalist, commentlist):
        print(username, vote, star, data, comment)

        sql = "SELECT * FROM douban_3 WHERE username = '{}'".format(username)
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        star_1 = 0
        star_2 = starl.index(star)+1
        for row in results:
            name = row[1]
            star_1 = row[3]
        if int(star_1) == int(star_2) and str(name) == str(username):
            print("该条记录已存在0---------------------------------------------")
        else:
            print('新记录+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            insert_sql = "INSERT INTO douban_3(username,vote,star,date,comment) VALUES('{}', '{}', '{}'," \
                         " '{}','{}')".format(username, vote, star_2, data, comment)
            try:
                cursor.execute(insert_sql)
                conn.commit()
            except:
                print('内容错误')


def cookie():
    '''
    loginUrl='https://accounts.douban.com/login'
    s=requests.session()
    print(s.cookies.get_dict())#先打印一下，此时一般应该是空的。
    postData={'form_email':'1336360448@qq.com','form_password':'133636wj','login':'登录'}
    rs=s.post(loginUrl, postData)
    c=requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
    c.set('cookie-name','cookie-value')
    s.cookies.update(c)
    print(s.cookies.get_dict())
    '''
    loginUrl = 'https://accounts.douban.com/login'
    s = req.session()
    postData = { 'form_email':'1336360448@qq.com','form_password':'133636wj','login':'登录', 'captcha-id': 'MoSD4wQrY0GGOxmspOBIkjkx:en',
                'captcha-solution': 'effect'}
    a = req.get(loginUrl)

    imagesrc = re.findall('<img id="captcha_image" src="(.*)" alt="captcha"', str(a.text))
    imgname = re.findall('<input type="hidden" name="captcha-id" value="(.*)"/>', str(a.text))
    print(imagesrc,imgname)
    postData = {'form_email': '1336360448@qq.com', 'form_password': '133636wj', 'login': '登录'}
    '''

    postData['captcha-id'] = imgname[0]
    code = input('code:')
    postData['captcha-solution'] = code
    print(postData)
    '''
    s = s.post(loginUrl, postData)
    c = req.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
    c.set('cookie-name', 'cookie-value')
    s.cookies.update(c)
    print(s.cookies.get_dict())
    return s.cookies.get_dict()


conn = pymysql.connect(host='172.18.0.2', user='root', passwd='123456', db='dou',charset='utf8')
cursor = conn.cursor()
cookies =cookie()

for i in start_urls:

    t = int(time.time())-39
    print(i)
    r = req.get(i, headers=headers, cookies=cookies)
    print(r.text)
    parse(r.text)
    break
conn.close()
