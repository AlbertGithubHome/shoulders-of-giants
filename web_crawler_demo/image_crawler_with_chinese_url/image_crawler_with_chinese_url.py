#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-12-20 15:31:45
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawl pictures with pretending browser

import urllib.request, re, os

# save file path
target_path = "images_crawler_results"
# target url that needs to crawler
target_url = "https://www.csdn.net/"
# request data headers
req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
}

def get_file_local_path(file_path):
    file_name = os.path.split(file_path)[1]
    return os.path.join(target_path, file_name)

def start_crawler():
    #create dir if not exist
    if not os.path.isdir(target_path):
        os.mkdir(target_path)

    req = urllib.request.Request(url = target_url, headers = req_headers)
    res = urllib.request.urlopen(req)
    data = res.read()

    for link, t in set(re.findall(r'(images.csdn.net[\S]*?(jpg|png|gif))', data.decode('utf8'))):
        reallink = 'https://' + urllib.request.quote(link)
        print(reallink)
        try:
            urllib.request.urlretrieve(reallink, get_file_local_path(link))
        except:
            print('crawler failed')

# start to crawler
if __name__ == '__main__':
    start_crawler()

def foo(n):
    for i in range(1, n+1):
        print(" "*(n-i) + "*"*(2*i-1))
foo(5)

sql = " where time ='CURRENT TIMESTAMP'"
print(sql)
newsql = sql.replace('\'', '')
print(newsql)

with open('mysql.txt', 'w') as file:
    file.write(sql)
    file.write("\n")
    file.write(newsql)

'''
content = 'images.csdn.net/20171219/\xe7\x8c\xaa\xe8\x84\xb8\xe5\xa4\xa7\xe5\x9b\xbe.jpg'
print(bytes(map(ord, content)).decode('utf8'))
print(urllib.request.quote(content))

content = 'images.csdn.net/20171218/336_280_\xe5\x89\xaf\xe6\x9c\xac.png'
print(bytes(map(ord, content)).decode('utf8'))
zw = bytes(map(ord, content)).decode('utf8')
print(zw)
print(urllib.request.quote(zw))
'''
