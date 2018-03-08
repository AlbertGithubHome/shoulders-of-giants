#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-22-28 14:39:55
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawler game step 2
# 
# 思路：遍历数字0-30作为密码，模拟post请求验证密码

'''
requests 是用Python语言编写，基于 urllib，采用 Apache2 Licensed 开源协议的 HTTP 库。
它比 urllib 更加方便，可以节约我们大量的工作，完全满足 HTTP 测试需求。
requests 的哲学是以 PEP 20 的习语为中心开发的，所以它比 urllib 更加 Pythoner。
更重要的一点是它支持 Python3 哦！
'''
import requests


# entrance url
target_url = 'http://www.heibanke.com/lesson/crawler_ex01/'

# recursively call this function
def try_website_password():
    password = 0
    while True:
        password = password + 1
        postdata = {'username': 'AlbertS', 'password': password}
        html = requests.post(target_url, postdata).content
        htmlcontent = html.decode('utf8')
        if '密码错误' not in htmlcontent:
            print("密码就是%d" % password)


# strart game step 2
if __name__ == '__main__':
    try_website_password()

'''
密码就是3
'''