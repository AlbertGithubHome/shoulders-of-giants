#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-03-14 19:42:05
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawler game step 4
# 
# 思路：就是尝试前面的密码0-30，
# 备注：1. 使用了美丽解析库：BeautifulSoup
#       2. 使用了库pandas，它依赖了lxml，需要手动安装一下
#       3. 使用了库pandas，它依赖了html5lib，需要手动安装一下


import requests
import pandas
from bs4 import BeautifulSoup
from threading import Thread


from PIL import Image
from PIL import ImageOps
import pytesseract
import subprocess
import re

# relative url
target_url = 'http://www.heibanke.com/lesson/crawler_ex'
login_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex'
img_url = 'http://www.heibanke.com/captcha/image/'

class crawler_client(object):

    def __init__(self, level_url, login_url, img_url, account="AlbertS", password="heibanke"):
        self.level_url_template = level_url
        self.login_url_template = login_url
        self.img_url = img_url
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

    def crawler_table_data(self):
        while self.count < 100:
            response = self.session.get(self.img_url)
            if response.ok:
                print("response.ok, current count =", self.count)
                df = pandas.read_html(response.content, encoding='utf-8')
                data = df[0] #获取第一个数据表格
                rownum = data.shape[0] # 获取表格行数
                for x in range(1,rownum):
                    if data.iloc[x][0] not in self.pwd_dict:
                        self.pwd_dict[data.iloc[x][0]] = data.iloc[x][1]
                        self.count = self.count + 1

                print(str(self.count) + '%' + self.count // 4 * '*')
                #print(self.pwd_dict); # 多线程时注释掉这一句，加上下面的else
            else:
                print(response, " is not ok!");

    def guess_password_with_normal(self, level):
        self.count = 0;
        self.pwd_dict = {};
        self.pwd_list = ['' for x in range(101)];
        # 注意这个101，不要越界
        # 还有这个空引号''，如果有值会导致密码错误

        self.crawler_table_data();

        for pos in self.pwd_dict.keys():
            self.pwd_list[int(pos)] = self.pwd_dict[pos]

        self.payload['password'] = int(''.join(self.pwd_list))
        print("password is", self.payload['password'])

        response = self.session.post(self.level_url, self.payload)
        bs_obj = BeautifulSoup(response.content, "html.parser")
        print(bs_obj.h3.string)


    def guess_password_with_thread(self, level, thread_num):
        self.count = 0;
        self.pwd_dict = {};
        self.pwd_list = ['' for x in range(101)];
        # 注意这个101，不要越界
        # 还有这个空引号''，如果有值会导致密码错误

        print("multiple thread handle method!")
        self.crawler_table_data();
        thread_list = [Thread(target=self.crawler_table_data) for i in range(thread_num)]
        for t in thread_list:
            print("start thread: %s\n" % t.name)
            t.start()

        for t in thread_list: # 等线程都关闭后再收集处理
            t.join()

        for pos in self.pwd_dict.keys():
            self.pwd_list[int(pos)] = self.pwd_dict[pos]

        self.payload['password'] = int(''.join(self.pwd_list))
        print("password is", self.payload['password'])

        response = self.session.post(self.level_url, self.payload)
        bs_obj = BeautifulSoup(response.content, "html.parser")
        print(bs_obj.h3.string)


    # 二值化算法
    def binarizing(self, image, threshold):
        pixdata = image.load()
        w, h = image.size
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return image

    # 识别图片文字
    def ocr_img(self, imagePath):
        image = Image.open(imagePath)
        #image.show()
        # tesseract 路径
        pytesseract.pytesseract.tesseract_cmd = 'H:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
        # 语言包目录和参数
        tessdata_dir_config = '--tessdata-dir "H:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 7 --user-words "./words_bed"'
        # lang 指定英文识别
        captcha = pytesseract.image_to_string(image, lang ='eng', config=tessdata_dir_config)
        captcha = captcha.replace(" ", "").replace("\n", "")
        if len(captcha) == 4 and captcha.isupper() and captcha.isalnum():
            print("try login, captcha is :", captcha)
            return captcha
        else:
            print("recognize failed, captcha is :", captcha)
        return False

    def simple_orc_img(self):
        image = Image.open("./cleanImage.png");
        # tesseract 路径
        pytesseract.pytesseract.tesseract_cmd = 'H:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
        # 语言包目录和参数
        tessdata_dir_config = '--tessdata-dir "H:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 7 --user-patterns "./pattern"'

        # lang 指定英文识别
        content = pytesseract.image_to_string(image, lang ='eng', config=tessdata_dir_config) #lang='eng'
        captchaResponse = content.replace(" ", "").replace("\n", "")
        print(captchaResponse)

    def get_captcha_image_name(self, response_content):
        image_name = re.findall(r'<img src="/captcha/image/(.*)/" alt="captcha"', response_content);
        return image_name[0]

    def save_and_clean_image(self, image_url, image_name):
        img_response = self.session.get(image_url)
        image_path_name = "./images/" + image_name
        with open(image_path_name + ".png", 'wb') as file:
            file.write(img_response.content)

        img = Image.open(image_path_name + ".png")
        # 转化为灰度图
        new_img = img.convert('L')
        # 把图片变成二值图像。
        new_img = self.binarizing(new_img, 190)
        new_img.save(image_path_name + "_clean.png")
        return image_path_name + "_clean.png"

    def test(self):
        response = self.session.get(self.level_url)
        if response.ok:
            image_name = self.get_captcha_image_name(response.content.decode('utf8'))
            print("image name is : " + image_name)
            image = self.save_and_clean_image(self.img_url + image_name, image_name)
            ret = self.ocr_img(image)
            print(ret)

    def get_captcha(self, max_count=50): # max_count是对于1个密码尝试识别验证码的次数
        for x in range(1, max_count):
            response = self.session.get(self.level_url)
            if response.ok:
                image_name = self.get_captcha_image_name(response.content.decode('utf8'))
                print("image name is : " + image_name)
                self.payload['captcha_0'] = image_name;

                image_path = self.save_and_clean_image(self.img_url + image_name, image_name)
                captcha = self.ocr_img(image_path)
                if captcha:
                    self.payload['captcha_1'] = captcha
                    break
            else:
                print("The network is disconnect, please try again later");
                time.sleep(10)
            time.sleep(3)






# strart game step 4
if __name__ == '__main__':
    crawler_game = crawler_client(target_url, login_url, img_url);
    #crawler_game.login_by_session('04');
    if True:
        crawler_game.login_by_session('04');
        crawler_game.get_captcha();
    else:
        #crawler_game.guess_password_with_thread('03', 8);
        #crawler_game.simple_orc_img();
        crawler_game.ocr_img();

# 第一次不用多线程的结果
'''
login csrftoken is iRUEFKQtYvDqNj0kgkQVtm1pvvh1CHkQ
login success : csrfmiddlewaretoken is drrUPkuKrVuWSZ0TtHcYqkwL2GI21WiN


login csrftoken is Ja0gDaBWQuw0LSdoneGzIeIGjKMwfKbl
login success : csrfmiddlewaretoken is o5vJn5WtzYZuxgLQP0uYaHANMGlXaiW4
image name is : 89f39f59ef5be1182879358d3c720445d1ab98a9
try login, captcha is : QVSE
QVSE
'''