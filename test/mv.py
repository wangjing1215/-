import requests as req
import time
import re
import pymysql

def get(url,flag):
    cookies = {'XLA_CI': '0be5bc19c36cf14ac83f5ce49934a7a2'}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    if flag==1:
        print('start to get')
    r = req.get(url, headers=headers, cookies=cookies)
    # print(r.content.decode('gbk'))
    if flag==1:
        print('end to get')
    try:
        resonse = r.content.decode('gbk', 'ignore')
    except:
        resonse = r.text.encode('utf8', 'ignore')
    return resonse

def parse(response):
    # print(response.body)
    print('*********************************')
    thehtml = str(response)
    # print(thehtml)
    namelist = re.findall('class="ulink">(.*)</a>', thehtml)
    linkurllist = re.findall('<a href="(.*)" class="ulink', thehtml)
    timelist = re.findall('<font color="#8F8C89">日期：(.*)\r', thehtml)
    #print(name, linkurl, time)
    downloadurllist=[]
    for lurl in linkurllist:
        lresponse=get('http://www.ygdy8.net'+lurl,0)
        lhtml = str(lresponse)
        downloadurl=re.findall('<a href="(.*)">ftp:', lhtml)
        try:
            downloadurllist.append(downloadurl[0])
        except:
            pass
    try:
        print(namelist[0], downloadurllist[0], timelist[0])
    except:
        return ''
    for name, url, time in zip(namelist, downloadurllist, timelist):
        print(name, url, time)

        sql = "SELECT * FROM mv WHERE name = '{}'".format(name)
        cursor.execute(sql)
        # 获取所有记录列表
        if cursor.execute(sql)==0:
            print('新记录+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            insert_sql = "INSERT INTO mv(name,linkurl,time) VALUES('{}', '{}', '{}')".format(name, url, time)
            try:
                cursor.execute(insert_sql)
                conn.commit()
            except:
                print('内容错误')
        else:
            print('已存在记录-------------------------------------------------')
            break


conn = pymysql.connect(host='172.18.0.2', user='root', passwd='123456', db='scrapy',charset='utf8')
cursor = conn.cursor()
try:
    for i in range(1,184):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'.format(str(i))
        print(url)
        resonse = get(url, 1)
        parse(resonse)
finally:
    conn.close()