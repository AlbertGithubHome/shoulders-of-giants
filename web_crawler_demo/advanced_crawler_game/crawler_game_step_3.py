#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-03-08 20:11:25
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawler game step 3
# 
# 思路：登录时添加了CSRF参数，利用session数据解决，allow_redirects是关键，目录最后有个字符'/'
# 如果不加'/'会出错，也就是不切页面，我也是服了，还没弄懂其中原因，可能是有post数据就需要加'/'

import requests

# relative url
target_url = 'http://www.heibanke.com/lesson/crawler_ex'
login_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex'

class crawler_client(object):

    def __init__(self, level_url, login_url, account="AlbertS", password="heibanke"):
        self.level_url_template = level_url
        self.login_url_template = login_url
        self.account = account
        self.password = password

    def login_by_session(self, level):
        self.level_url = self.level_url_template + level + '/'
        self.login_url = self.login_url_template + level + '/'

        self.session = requests.session()
        self.csrftoken = self.session.get(self.login_url).cookies['csrftoken']
        print("login csrftoken is", self.csrftoken)

        self.payload = {'username': self.account, 'password': self.password, 'csrfmiddlewaretoken': self.csrftoken}
        self.payload['csrfmiddlewaretoken'] = self.session.post(self.login_url, self.payload).cookies['csrftoken']
        print("login success : csrfmiddlewaretoken is", self.payload['csrfmiddlewaretoken'])

    def login_by_cookies(self, level):
        self.level_url = self.level_url_template + level + '/'
        self.login_url = self.login_url_template + level + '/'

        self.cookies = requests.get(self.login_url).cookies
        self.payload = {'username': self.account, 'password': self.password, 'csrfmiddlewaretoken': self.cookies['csrftoken']}

        self.cookies = requests.post(self.login_url, data=self.payload, allow_redirects=False, cookies=self.cookies).cookies
        self.payload['csrfmiddlewaretoken'] = self.cookies['csrftoken'];
        print("login success : csrfmiddlewaretoken is", self.payload['csrfmiddlewaretoken'])


    def guess_password_by_session(self, level):
        for try_value in range(30):
            self.payload['password'] = try_value;
            html = self.session.post(self.level_url, self.payload).content
            htmlcontent = html.decode('utf8')

            if '密码错误' not in htmlcontent:
                print("密码就是%d" % try_value)
                break;
            else:
                print("密码%d with session尝试错误..." % try_value)

    def guess_password_by_cookies(self, level):
        for try_value in range(31):
            self.payload['password'] = try_value;
            html = requests.post(self.level_url, self.payload, cookies=self.cookies).content
            htmlcontent = html.decode('utf8')

            if '密码错误' not in htmlcontent:
                print("密码就是%d" % try_value)
                break;
            else:
                print("密码%d with cookies尝试错误..." % try_value)


# strart game step 3
if __name__ == '__main__':
    crawler_game = crawler_client(target_url, login_url);
    if False:
        crawler_game.login_by_session('02');
        crawler_game.guess_password_by_session('02');
    else:
        crawler_game.login_by_cookies('02');
        crawler_game.guess_password_by_cookies('02');

'''
login csrftoken is a7bGzT1maKElmEiIZeGisUDqFw1r2MO5
login success : csrfmiddlewaretoken is f5sQfCmvULrPculc27C4kvAQQrRmIE9h
密码0 with session尝试错误...
密码1 with session尝试错误...
密码2 with session尝试错误...
密码3 with session尝试错误...
密码4 with session尝试错误...
密码5 with session尝试错误...
密码6 with session尝试错误...
密码7 with session尝试错误...
密码8 with session尝试错误...
密码9 with session尝试错误...
密码10 with session尝试错误...
密码11 with session尝试错误...
密码12 with session尝试错误...
密码13 with session尝试错误...
密码14 with session尝试错误...
密码15 with session尝试错误...
密码16 with session尝试错误...
密码就是17
'''

'''
login success : csrfmiddlewaretoken is WIvOQBciraTyYzZFE1azJYl6I4UvtMp7
密码0 with cookies尝试错误...
密码1 with cookies尝试错误...
密码2 with cookies尝试错误...
密码3 with cookies尝试错误...
密码4 with cookies尝试错误...
密码5 with cookies尝试错误...
密码6 with cookies尝试错误...
密码7 with cookies尝试错误...
密码8 with cookies尝试错误...
密码9 with cookies尝试错误...
密码10 with cookies尝试错误...
密码11 with cookies尝试错误...
密码12 with cookies尝试错误...
密码13 with cookies尝试错误...
密码14 with cookies尝试错误...
密码15 with cookies尝试错误...
密码16 with cookies尝试错误...
密码就是17
'''

'''
for try_value in range(30):
    print(try_value)

结果是0,1,2...28,29
'''