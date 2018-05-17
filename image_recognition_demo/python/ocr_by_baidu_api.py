#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-03-28 20:16:23
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : recognize image
# 
# 思路：直接使用百度ORC库的的Python版本API进行识别
#       
# 备注：1. 使用了百度OCR API ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
#       2. 需要安装百度API，参考地址：https://cloud.baidu.com/doc/OCR/OCR-Python-SDK.html#.E5.BF.AB.E9.80.9F.E5.85.A5.E9.97.A8
#       3. 如果已安装pip，执行pip install baidu-aip即可；如果已安装setuptools，执行python setup.py install即可。


from aip import AipOcr

class image_orc_machine(object):

    # app_id、api_key 和 api_secret 需要修改成自己在百度注册应用对应的数据，默认数据无效
    def __init__(self, app_id = '10943424', api_key="bEDC0GG4GH9BptPnUzvZgzXN", api_secret='byEUrIyMnSLhx2WIyKksICOmhKKCrKE5'):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret

    # 读取图片数据
    def get_file_content(self, image_path):
        with open(image_path, 'rb') as fp:
            return fp.read()

    # 识别图片文字
    def ocr_img(self, image_path):
        # 创建百度OCR客户端
        orc_client = AipOcr(self.app_id, self.api_key, self.api_secret)
        # 识别并返回结果
        result_json = orc_client.basicGeneral(self.get_file_content(image_path));

        if 'words_result' in result_json.keys():
            # 循环统计识别结果
            captcha = ''
            for word_pair in result_json['words_result']:
                captcha += word_pair['words']

            print("recognize content is :", captcha)
        else:
            # 结果有误
            print("recognize content is :", result_json)

# strart image recognition
if __name__ == '__main__':
    image_orc_client = image_orc_machine();
    image_orc_client.ocr_img('../images/target0.png');


# 简单识别结果错误，与百度Web的API应该是调用的相同接口，但是速度比Web快，识别英文不如pytesseract
'''
recognize content is : ALSE
[Finished in 1.6s]
'''

# 百度API版本
'''
上线日期    版本号     更新内容
2018.01.12  2.1.0   新增自定义OCR识别
2017.12.22  2.0.0   SDK代码重构
2017.8.25   1.6.4   OCR 新增营业执照识别
2017.5.11   1.0.0   OCR服务上线
'''

#百度API安装提示
'''
>pip install baidu-aip
Collecting baidu-aip
  Downloading baidu-aip-2.2.0.0.tar.gz
Requirement already satisfied: requests in h:\program files\python\python35-32\lib\site-packages (from baidu-aip)
Requirement already satisfied: urllib3<1.23,>=1.21.1 in h:\program files\python\python35-32\lib\site-packages (from requests->baidu-aip)
Requirement already satisfied: certifi>=2017.4.17 in h:\program files\python\python35-32\lib\site-packages (from requests->baidu-aip)
Requirement already satisfied: idna<2.6,>=2.5 in h:\program files\python\python35-32\lib\site-packages (from requests->baidu-aip)
Requirement already satisfied: chardet<3.1.0,>=3.0.2 in h:\program files\python\python35-32\lib\site-packages (from requests->baidu-aip)
Installing collected packages: baidu-aip
  Running setup.py install for baidu-aip ... done
Successfully installed baidu-aip-2.2.0.0
You are using pip version 9.0.1, however version 9.0.3 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.
'''