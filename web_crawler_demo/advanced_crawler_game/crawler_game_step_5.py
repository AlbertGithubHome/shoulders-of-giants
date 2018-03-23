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
#
# 尝试  1. 真正花时间较多的是处理验证码识别，现在代码中使用的是pytesseract库中的默认识别
#       2. 其实这也是一种解决方案，还可以使用百度的图片识字服务，后续可以继续补充
#       3. 期间还遇到一个坑就是下载验证码图片，将get返回的bytes数组转换成图片花了一些时间
#       4. 一开始下载图片的时候想把bytes直接转为image，没有实现只能保存成.png再用Image打开了
#       5. 期间出现了编码错误UnicodeEncodeError: 'gbk' codec can't encode character '\u20ac' in position 1: illegal multibyte sequence
#       6. 上述错误主要是验证码识别结果包含错误字符，输出到命令行时报错
# 
# 结果  1. 前几次因为验证码中包含特殊字符，输出错误，导致崩溃
#       2. 第一次成功耗时384.5s，速度还可以吧

from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import requests
import time
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
        captcha = captcha.replace(" ", "").replace("\n", "").replace("0", "O").replace("1", "I")
        if len(captcha) == 4 and captcha.isupper() and captcha.isalnum():
            print("try login, captcha is :", captcha)
            return captcha
        else:
            #if captcha.isalnum(): # 只显示字母和数字的，不然会报错
            #只显示字母和数字还是会报错，干脆不显示了
            if False:
                print("recognize failed, captcha is :", captcha)
            else:
                print("recognize failed")
        return False


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


    def get_captcha(self, max_count=50): # max_count是对于1个密码尝试识别验证码的次数
        for x in range(1, max_count):
            response = self.session.get(self.level_url)
            if response.ok:
                # 有下载了一张图片
                self.recognize_img_sum += 1
                image_name = self.get_captcha_image_name(response.content.decode('utf8'))
                print("image name is : " + image_name)
                # captcha_0的值就是图片的名字
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

    def guess_password_with_normal(self, level):
        # 记录识别验证码的数量
        self.recognize_img_sum = 0
        # 循环查找密码0-30
        for try_pass in range(31):
            # 对于每个密码，必须找到密码错误才停止，否则都是验证码错误
            while True:
                self.payload['password'] = try_pass;
                print("try password is", try_pass)
                # 识别验证码
                self.get_captcha()

                response = self.session.post(self.level_url, self.payload)
                bs_obj = BeautifulSoup(response.content, "html.parser")

                # 密码错误即可验证下一个密码
                if '密码错误' in bs_obj.h3.string:
                    break;
                elif '成功' in bs_obj.h3.string:
                    print("password is finded successfully")
                    print("password is : %d, captcha is : %s" % (try_pass, self.payload['captcha_1']))
                    print("recognize image count is %d, recognize successfully count is : %s" % (self.recognize_img_sum, try_pass + 1))
                    print("html h3 content is :", bs_obj.h3.string)
                    return 'ok';
                else: # 走到这个分支说明是验证码错误，需要重新识别验证码
                    pass


# strart game step 5
if __name__ == '__main__':
    crawler_game = crawler_client(target_url, login_url, img_url);
    crawler_game.login_by_session('04');
    crawler_game.guess_password_with_normal('04');


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

# 第一次完整的验证
'''
login csrftoken is xYk1JtHMPS3u7GohIjuHVbHZfluaEXym
login success : csrfmiddlewaretoken is 09mQoGUlpf9MNbiVq30ip85RHlM3ipBo
try password is 0
image name is : 4cb684fb7f41bad597429c1bdd82805fc580b7a2
recognize failed
image name is : 68739dd43e7dd1271a7c04e067cc968c9f9170fb
recognize failed
image name is : 8a9ccbe120bfa6de2be99a84471f9c0ec3d36d5e
try login, captcha is : NGFP
try password is 1
image name is : db413ba25c29ba3a210bd98f909bcc8f32172a50
recognize failed
image name is : 0f1ea3af49d0860a6a708294f60f2f8bd6b5412a
try login, captcha is : GCCI
try password is 2
image name is : 7463d6b999c4a6ccd6c1c24b9d1837699825ce14
recognize failed
image name is : bfe033ddfa505d5d2ee209d542e589d2a8c89766
recognize failed
image name is : 2047d85648361bd2969b9ecb7e6d445504c9eca0
try login, captcha is : BOVO
try password is 2
image name is : bd895244729999dc919cb02dce64434771d15814
recognize failed
image name is : 6d67a60d512399f6c498bd51b85956f4daee4fa8
recognize failed
image name is : 24707c2bf6ac5444447c6bee9535a8ed100d5c70
try login, captcha is : GQQZ
try password is 2
image name is : f4dd5f95e527722f1ec06ac204174315d63d08e9
recognize failed
image name is : 78758db47c04caf08b06432388103cb270295719
recognize failed
image name is : e325316708b36b0b62acacc4c6e753613c0be6b4
try login, captcha is : OSWD
try password is 3
image name is : c98a6cd663af4942163a383638e7cc3b20fe0084
try login, captcha is : AQGE
try password is 4
image name is : 4d8804e35f245b52e6bf7a06bb92d1444ce04dcc
try login, captcha is : OSNO
try password is 4
image name is : b2d15f689374b4b1d482bbd52dc2b53122130051
recognize failed
image name is : 1e2c22123e935bac62fbc4bf4d15c780c1799e49
recognize failed
image name is : 6ea3c96bcad71b1a6bf504279a2bd0b1d4dcba26
recognize failed
image name is : f053bde001fb0dc82b96ea52d2e404e8e5764025
recognize failed
image name is : 5750d0a18df6f739db18057f494af16d9edaba3a
try login, captcha is : UNBN
try password is 5
image name is : fd091287b1baaf0675f9b1a71b35574d7a4750cd
recognize failed
image name is : a2e6da8ecd1fdba5f658aa4a065444484b6362b7
recognize failed
image name is : 8433faf5fdd18f2189566239d2c16b50f075e611
try login, captcha is : K986
try password is 5
image name is : d25d89bb8a4c32acdcd36e107fe52c50791ea7f2
recognize failed
image name is : d79c2f713d24312358756f65d04a33a71a954fa0
try login, captcha is : LRMU
try password is 6
image name is : 24c14544eecaebfb233750cabdf131c6ba06eb80
recognize failed
image name is : 34c63aa1d86a99746e5892877ec6dcc0f393d94c
recognize failed
image name is : a4a15ac81640391e3a32912bc1257c4184cc4281
recognize failed
image name is : 7421b814a9d43b7a0b330e7a37b29397f2ef7d9e
recognize failed
image name is : 93d3ee0348edf787d2101bf0bead58cb4feb26f8
try login, captcha is : WPEB
try password is 7
image name is : ae097c2c4f219e5bab32921d5ce8dece01228763
recognize failed
image name is : aaf6e5d2da9d79f7883cbfe97edef74ab8d4c285
recognize failed
image name is : dcdf415d79742e1694eaf5a1c3067b205ba1dda5
recognize failed
image name is : 4df9fb2e8810754049fe5e613792e3114049c0de
recognize failed
image name is : 222717c31c32433baad2acd6d0cc5344bd6540ec
try login, captcha is : MVCC
try password is 7
image name is : ecbd2cdce90859918f7d3fbc22198b79b71eb5ec
recognize failed
image name is : fe830ea607c9e6d729901e95345ab1ed2221256d
recognize failed
image name is : fe5ea4d26e53d56fb9962b71bc3577befccbb4d0
recognize failed
image name is : 53cdbe8f37506557a496eac02f4538fd288ee4a5
recognize failed
image name is : c18f37d934007c18ceca2983473b2b978e82aed6
recognize failed
image name is : f91c06b2c82ae74e15f6447ad82bc48862bc552c
try login, captcha is : NOOA
try password is 7
image name is : 3e3789af33cc27d7521ef58cb6e510dfa973d7cb
recognize failed
image name is : 6e474649046faeccb272486f09e44ef571d95e1b
recognize failed
image name is : 5cf231ca159430eee04543ad59035a5059cdb2dd
try login, captcha is : VQMM
try password is 7
image name is : 8e91d627edf127901fcd02b7cf717d21540a824e
recognize failed
image name is : 74b38caf19b6ceabda6568e4ac6cc7033327a4c9
recognize failed
image name is : c57c9970c1af39c314b73ebace1879f84419b05d
recognize failed
image name is : 4b14806b34d1d6e8037c61fae4cc682debda843b
recognize failed
image name is : b8dc5f6b1b3c49eefd2b0be7e1d2b92ec1c97844
recognize failed
image name is : 45f6cde0e4dac8fba18780339a3cb13afe105f9e
recognize failed
image name is : ee8431c371a9d01c44906b565f008abd5e4a49fe
recognize failed
image name is : 644589d2f50fa4603fedad1ef09340b8decb0266
try login, captcha is : CODE
try password is 7
image name is : 2a870f329b1ca2dad06aeaa112dcb51ce7232629
recognize failed
image name is : eaa45f85dfc08ef88fe618abdb1c189bef41c616
try login, captcha is : 9OO8
try password is 7
image name is : 879088bba24b0debf02ad26102ef3cea4c1464c1
recognize failed
image name is : b32367da223f4c1d395d810660291a36b9451c7b
recognize failed
image name is : 12aba04561fd61eb9cf995975856de954fb86d07
try login, captcha is : KQXP
try password is 7
image name is : 61ef94852a9e676c9fcd429e5094c2e32237e7fa
recognize failed
image name is : 0e419b6a456f73e78788099d202dd8eecc74a910
recognize failed
image name is : ebac14bcc4f7b1190b650fee00a014eef2e0f7db
recognize failed
image name is : 0765c6787bbf7cf6dc27ed98c9bfde539c8cbaf7
recognize failed
image name is : 7d545203417d90c606747d72afd6380dd7d5389d
try login, captcha is : GOIH
try password is 7
image name is : 6613a7222b75023e0ba77ed9faf10d1eb959b2b4
recognize failed
image name is : 78391edc4a557c734db190c19f6f6aee5ef7baec
try login, captcha is : VMAY
try password is 8
image name is : c16f07761fbdbf146dbb180b4d5152c2af0b8954
try login, captcha is : XXBS
try password is 9
image name is : 59ec5c434f8ca8be99cf79c1a19d3a92cb72d96e
try login, captcha is : CEQQ
try password is 9
image name is : dad8276713fc835be571d4ff01031614234f41b9
recognize failed
image name is : b434ccdc1e13aa608d355c05ec65cd8b71da43b2
recognize failed
image name is : e0babf9f5877cbeff37128b7637e1b9943d6a24f
recognize failed
image name is : 1bd66b804361e1d59a1d7f6670da88bd45db961b
recognize failed
image name is : 8687631dbda0e0b822d5ce31a36b9aa721a0530e
recognize failed
image name is : 89889b0715d564e01d7921a74a3bed83a5558bd2
recognize failed
image name is : 8afa45d2ecb398980818aebc432ac3678af65e07
recognize failed
image name is : 0344fe5377d6953f75e04eac1e0ac5ac8156209a
try login, captcha is : MYUJ
try password is 9
image name is : 6e3d982cf6f71d6c9b16fab898b17a0ec20a3aad
recognize failed
image name is : 1c6f2852ab39584162c5f79edae28507e108a54c
try login, captcha is : OGIG
try password is 9
image name is : ddfea5b727e55dc9485a7198d6deece5800bfe0e
try login, captcha is : RTLO
password is finded successfully
password is : 9, captcha is : RTLO
recognize image count is 78, recognize successfully count is : 10
html h3 content is : 恭喜! 用户AlbertS成功闯关, 后续关卡敬请期待
[Finished in 384.5s]
'''