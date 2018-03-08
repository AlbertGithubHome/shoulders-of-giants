#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-03-08 20:11:25
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawler game step 3
# 
# 思路：登录时添加了CSRF参数，利用session数据解决

import requests

# entrance url
target_url = 'http://www.heibanke.com/lesson/crawler_ex'
login_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex'

class crawler_client(object):

    def __init__(self, level_url, login_url, account="AlbertS", password="heibanke"):
        self.level_url_template = level_url
        self.login_url_template = login_url
        self.account = account
        self.password = password

    def login(self, level):
        self.level_url = self.level_url_template + level
        self.login_url = self.login_url_template + level
        self.session = requests.session()

        self.csrftoken = self.session.get(self.login_url).cookies['csrftoken']
        print("login csrftoken is", self.csrftoken)



# entrance url
target_url = 'http://www.heibanke.com/lesson/crawler_ex02/'

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
            break;

        if password > 30:
            break;


# strart game step 3
if __name__ == '__main__':
    crawler_game = crawler_client(target_url, login_url);
    crawler_game.login('03')
    

'''
密码就是3
'''