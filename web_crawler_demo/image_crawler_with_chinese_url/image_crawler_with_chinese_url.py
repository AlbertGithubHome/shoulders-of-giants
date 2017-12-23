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
