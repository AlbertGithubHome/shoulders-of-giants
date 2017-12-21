#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-12-21 19:49:40
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawler game step 1

import re
import urllib.request
from bs4 import BeautifulSoup
# BeautifulSoup 是一个新接触的Python库
# 它可以把html解析的非常美丽

# entrance url
target_url = 'http://www.heibanke.com/lesson/crawler_ex00/'

# recursively call this function
def open_next_page(sub_url):
    req = urllib.request.Request(url = target_url + sub_url)
    res = urllib.request.urlopen(req)
    # "html.parser"表示解析网站内容
    bs_obj = BeautifulSoup(res.read(), "html.parser")
    # find number list in html content
    number_list = re.findall(r'\d+', bs_obj.h3.string)
    print(bs_obj.h3.string)
    if number_list:
        open_next_page(number_list[0])

# strart game
if __name__ == '__main__':
    open_next_page('')

'''
你需要在网址后输入数字99039
下一个你需要输入的数字是48743. 
下一个你需要输入的数字是26048. 
下一个你需要输入的数字是43713. 
下一个你需要输入的数字是48776. 还有一大波数字马上就要到来...
下一个你需要输入的数字是61813. 还有一大波数字马上就要到来...
下一个你需要输入的数字是69634. 还有一大波数字马上就要到来...
下一个你需要输入的数字是49163. 还有一大波数字马上就要到来...
下一个你需要输入的数字是26470. 还有一大波数字马上就要到来...
下一个你需要输入的数字是64899. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是36702. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是83105. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是25338. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是19016. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是13579. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是43396. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是39642. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是96911. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是30965. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是67917. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是22213. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是72586. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是48151. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是53639. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是10963. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是65392. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是36133. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是72324. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是57633. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是91251. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是87016. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是77055. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是30366. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是83679. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是31388. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是99446. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是69428. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是34798. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是16780. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是36499. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是21070. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是96749. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是71822. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是48739. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是62816. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是80182. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是68171. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是45458. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是56056. 老实告诉你吧, 这样的数字还有上百个
下一个你需要输入的数字是87450. 老实告诉你吧, 这样的数字还有上百个
恭喜你,你找到了答案.继续你的爬虫之旅吧
'''