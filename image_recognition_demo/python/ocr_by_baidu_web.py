#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-03-28 20:09:17
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : recognize image
# 
# 思路：首先将图片进行二值化处理，然后使用百度ORC库的网页API进行识别
#       
# 备注：1. 使用了百度OCR API ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可


from PIL import Image
import requests
import base64
import io

class image_orc_machine(object):

    # api_key 和 api_secret 需要修改成自己在百度注册应用对应的数据，默认数据无效
    def __init__(self, api_key="bEDC0GG4GH9BptPnUzvZgzXN", api_secret='byEUrIyMnSLhx2WIyKksICOmhKKCrKE5'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_url = 'https://aip.baidubce.com/oauth/2.0/token'
        self.token_param = '?grant_type=client_credentials&client_id='+api_key+'&client_secret='+api_secret
        self.token_header = { 'Content-Type':'application/json;charset=UTF-8' }
        self.ocr_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'

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
        
        # 二进制流用来存储图片数据
        img_bytes = io.BytesIO()
        new_img.save(img_bytes, format='PNG')
        base64_data = base64.b64encode(img_bytes.getvalue())

        # 获取token
        response_json = requests.get(url=self.token_url+self.token_param, headers=self.token_header).json()
        # 发起图片识别请求
        response_json = requests.post(self.ocr_url, 
            params={'access_token': response_json['access_token']}, 
            data={'image': base64_data}).json()

        # 循环统计识别结果
        captcha = ''
        for word_pair in response_json['words_result']:
            captcha += word_pair['words']

        print("recognize content is :", captcha)

# strart image recognition
if __name__ == '__main__':
    image_orc_client = image_orc_machine();
    image_orc_client.ocr_img('../images/target0.png');


# 识别结果错误，识别英文不如pytesseract
'''
recognize content is : ALSE
[Finished in 5.8s]
'''