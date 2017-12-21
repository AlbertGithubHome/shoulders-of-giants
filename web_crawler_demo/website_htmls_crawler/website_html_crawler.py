#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-12-20 15:31:45
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawl htmls with pretending browser

import urllib.request, socket, re, sys, os, time, random
from io import BytesIO

# save file path
target_path = "htmls_crawler_results"
target_url = "http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'
}

headers_list = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36',
    'Opera/9.25 (Windows NT 5.1; U; en)',  
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
]

def test_encode():
    print('中文'.encode('utf-8'))
    print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))

    # this operation is very important
    print(bytes(map(ord, '\xe4\xb8\xad\xe6\x96\x87')))
    bytes_content = bytes(map(ord, '\xe4\xb8\xad\xe6\x96\x87'))
    print(bytes_content.decode('utf-8'))
    # output result:
    # b'\xe4\xb8\xad\xe6\x96\x87'
    # 中文
    # b'\xe4\xb8\xad\xe6\x96\x87'
    # 中文

def crawler_html(url_path):
    #req = urllib.request.Request(url = url_path, headers = req_headers)
    req = urllib.request.Request(url = url_path)
    temp_agent = random.choice(headers_list)
    print(temp_agent)
    req.add_header('User-Agent', temp_agent)
    res = urllib.request.urlopen(req)
    data = res.read()

    title = list(re.findall(r'(?<=<h4>).+?(?=</h4>)', data.decode('utf-8')))[0]
    # test encode and decode a long time
    # test_encode()

    title = title.replace('/', '_')
    with open(os.path.join(target_path, title) + '.html', 'wb') as file:
        file.write(data)


def start_crawler():
    #create dir if not exist
    if not os.path.isdir(target_path):
        os.mkdir(target_path)

    # make request
    req = urllib.request.Request(url = target_url, headers = req_headers)
    res = urllib.request.urlopen(req)
    data = res.read()

    # find url of htmls
    url_set = set(re.findall(r'(wiki/[\S]*(?="))', str(data)))
    url_list = list(map(lambda x : 'http://www.liaoxuefeng.com/' + x, url_set))

    all_url = '\n'.join(url_list)
    print('total article count =', len(url_set))

    # all htmls url to files
    with open('www.liaoxuefeng.com_python.txt', 'w') as file:
        file.write(all_url)

    # crawler html by loop
    count = 0
    for url in url_list:
        time.sleep(15)
        crawler_html(url)
        print(url)
        count = count + 1
        print('finish article :', count)

# start to crawler
if __name__ == '__main__':
    start_crawler()


