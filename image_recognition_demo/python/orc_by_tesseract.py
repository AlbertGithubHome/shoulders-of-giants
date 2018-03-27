#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-03-27 15:48:03
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : recognize image
# 
# 思路：首先将图片进行二值化处理，然后使用pytesseract库中函数进行识别
#       
# 备注：1. 使用了OCR库，需要import pytesseract
#       2. 当前测试环境是Windows，需要单独安装谷歌 Tesseract
#       3. 安装版：https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.01.exe
#       4. 免装版：https://github.com/parrot-office/tesseract/releases/download/3.5.1/tesseract-Win64.zip
#       5. 免安装版需要下载中文语言包，放置到Tesseract的tessdata目录下
#       6. 其他操作系统参考： https://github.com/tesseract-ocr/tesseract/wiki
#  

from PIL import Image
import pytesseract

class image_orc_machine(object):

    def __init__(self, default_way="tesseract"):
        self.default_way = default_way

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
    def ocr_img(self, image_path):
        image = Image.open(image_path)
        # 转化为灰度图
        new_img = image.convert('L')
        # 把图片变成二值图像。
        new_img = self.binarizing(new_img, 190)
        # tesseract 路径
        pytesseract.pytesseract.tesseract_cmd = 'H:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
        # 语言包目录和参数
        tessdata_dir_config = '--tessdata-dir "H:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 7'
        # lang 指定英文识别
        captcha = pytesseract.image_to_string(new_img, lang ='eng', config=tessdata_dir_config)
        print("recognize content is :", captcha)

# strart image recognition
if __name__ == '__main__':
    image_orc_client = image_orc_machine();
    image_orc_client.ocr_img('../images/target0.png');

# 识别结果
'''
recognize content is : QVSE
[Finished in 3.1s]
'''