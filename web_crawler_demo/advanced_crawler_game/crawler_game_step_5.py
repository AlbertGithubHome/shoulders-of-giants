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
#       


import requests
import pandas
from bs4 import BeautifulSoup
from threading import Thread


from PIL import Image
from PIL import ImageOps
import pytesseract
import subprocess

# relative url
target_url = 'http://www.heibanke.com/lesson/crawler_ex'
login_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex'
pwd_url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list'

class crawler_client(object):

    def __init__(self, level_url, login_url, pwd_url, account="AlbertS", password="heibanke"):
        self.level_url_template = level_url
        self.login_url_template = login_url
        self.pwd_url = pwd_url
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
            response = self.session.get(self.pwd_url)
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
    def binarizing(self, img, threshold):
        pixdata = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img

    # 识别图片文字
    def ocr_img(self):

        # 打开图片
        image = Image.open("./verification.png")
        # image = Image.open("./test.png")
        new_im = image.crop((0, 0, 92, 36))
        # 转化为灰度图
        new_im = new_im.convert('L')
        # 把图片变成二值图像。
        new_im = self.binarizing(new_im, 190)
        #new_im.show()
        #return new_im;

        # tesseract 路径
        pytesseract.pytesseract.tesseract_cmd = 'H:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
        # 语言包目录和参数
        #tessdata_dir_config = '--tessdata-dir "H:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 3'
        tessdata_dir_config = '--tessdata-dir "H:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

        # lang 指定英文识别
        question = pytesseract.image_to_string(new_im, lang='eng', config=tessdata_dir_config)
        #question = question.replace("\n", "")[2:]

        print(question);

    def simple_orc_img(self):
        image = Image.open("./cleanImage.png");
        # tesseract 路径
        pytesseract.pytesseract.tesseract_cmd = 'H:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
        # 语言包目录和参数
        tessdata_dir_config = '--tessdata-dir "H:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 7 --user-patterns "./pattern"'

        # lang 指定英文识别
        content = pytesseract.image_to_string(image, lang ='eng', config=tessdata_dir_config) #lang='eng'
        print(content)


    def get_captcha(self, imagePath):
        print(u'开始识别{}中的验证码:'.format(imagePath))
        try:
            p = subprocess.Popen(["tesseract", imagePath, 'captcha'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
        except:
            print('subprocess error')
        with open('captcha.txt', "r") as f:
            captchaResponse = f.read().replace(" ", "").replace("\n", "")

        if len(captchaResponse) == 4 and captchaResponse.isupper() and captchaResponse.isalnum():
            print(u'识别结果:{},尝试登录'.format(captchaResponse))
            return captchaResponse
        else:
            print(captchaResponse,u'识别失败...')
        return 0

    def cleanImage(self, imagePath):
        print(u'清洗图片:{}...'.format(imagePath))
        image = Image.open(imagePath)
        image = image.point(lambda x: 0 if x < 143 else 255)
        borderImage = ImageOps.expand(image, border=20, fill='white')
        borderImage.save("./cleanImage2.png")
        print('Done')



# strart game step 4
if __name__ == '__main__':
    crawler_game = crawler_client(target_url, login_url, pwd_url);
    #crawler_game.login_by_session('03');
    if False:
        crawler_game.guess_password_with_normal('03');
    else:
        #crawler_game.guess_password_with_thread('03', 8);
        crawler_game.simple_orc_img();
        #crawler_game.cleanImage("./cleanImage.png");

# 第一次不用多线程的结果
'''
login csrftoken is iRUEFKQtYvDqNj0kgkQVtm1pvvh1CHkQ
login success : csrfmiddlewaretoken is drrUPkuKrVuWSZ0TtHcYqkwL2GI21WiN
'''