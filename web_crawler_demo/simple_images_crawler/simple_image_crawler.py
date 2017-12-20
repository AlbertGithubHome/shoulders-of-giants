#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-12-20 15:31:45
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : crawl pictures with pretending browser

import urllib.request, socket, re, sys, os

# save file path
target_path = "images_crawler_results"
# target url that needs to crawler
target_url = "https://www.douban.com/"
# request data headers
req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'
}

def get_file_local_path(file_path):
    file_name = os.path.split(file_path)[1]
    return os.path.join(target_path, file_name)

def start_crawler():
    #create dir if not exist
    if not os.path.isdir(target_path):
        os.mkdir(target_path)

    req = urllib.request.Request(url = target_url, headers = req_headers)
    res = urllib.request.urlopen(req)
    data = res.read()

    for link, t in set(re.findall(r'(https:[\S]*?(jpg|png|gif))', str(data))):
        print(link)
        try:
            urllib.request.urlretrieve(link, get_file_local_path(link))
        except:
            print('crawler failed')

# start to crawler
if __name__ == '__main__':
    start_crawler()


# crawler result:
'''
https://img3.doubanio.com/img/songlist/large/354640-2.jpg
https://img3.doubanio.com/img/songlist/large/12049-1.jpg
https://img3.doubanio.com/dae/niffler/niffler/images/6da43bc4-cdd7-11e7-bb25-0242ac110014.png
https://img3.doubanio.com/view/dianpu_product_item/medium/public/p377790.jpg
https://img3.doubanio.com/view/photo/albumcover/public/p2505522515.jpg
https://img1.doubanio.com/dae/niffler/niffler/images/4ed34930-d4b5-11e7-91bc-0242ac110018.jpg
https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2506935748.jpg
https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2504277551.jpg
https://img3.doubanio.com/view/site/small/public/bc53b04961e0645.jpg
https://img1.doubanio.com/spic/s29620879.jpg
https://img3.doubanio.com/view/event_poster/small/public/c5172363511b4e3.jpg
https://img3.doubanio.com/view/dianpu_shop_icon/medium/public/2e35f89d2c7990d.jpg
https://img3.doubanio.com/img/files/file-1423193113.png
https://img1.doubanio.com/dae/niffler/niffler/images/b5d54766-c3ab-11e7-9bba-0242ac110008.jpg
https://img3.doubanio.com/view/site/small/public/c9de2df9b95e314.jpg
https://img3.doubanio.com/dae/niffler/niffler/images/d3f40a18-9f78-11e7-b531-0242ac11002d.png
https://img3.doubanio.com/spic/s29602845.jpg
https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2507566212.jpg
https://img3.doubanio.com/view/event_poster/small/public/2e1cd988eaf895e.jpg
https://img3.doubanio.com/img/files/file-1489464722.jpg
https://img1.doubanio.com/icon/g170177-27.jpg
https://img1.doubanio.com/view/event_poster/small/public/9dc033f825d983c.jpg
https://img3.doubanio.com/icon/g20618-4.jpg
https://img3.doubanio.com/view/site/small/public/8e96b7c701473d3.jpg
https://img3.doubanio.com/mpic/s29615583.jpg
https://img3.doubanio.com/view/dianpu_product_item/medium/public/p270364.jpg
https://img3.doubanio.com/img/songlist/large/471009-2.jpg
https://img3.doubanio.com/img/files/file-1495708840.jpg
https://img1.doubanio.com/view/dianpu_product_item/medium/public/p1982227.jpg
https://img1.doubanio.com/img/files/file-1478594087.jpg
https://img3.doubanio.com/f/sns/0c708de69ce692883c1310053c5748c538938cb0/pics/sns/anony_home/icon_qrcode_green.png
https://img3.doubanio.com/dae/niffler/niffler/images/f90e218a-b8aa-11e7-9cc5-0242ac110021.jpg
https://img3.doubanio.com/dae/niffler/niffler/images/1c148a64-c50a-11e7-953c-0242ac110012.jpg
https://img3.doubanio.com/view/photo/albumcover/public/p2162936775.jpg
https://img3.doubanio.com/view/dianpu_product_item/medium/public/p458880.jpg
https://img3.doubanio.com/view/dianpu_product_item/medium/public/p521646.jpg
https://www.douban.com/pics/blank.gif
https://img3.doubanio.com/view/dianpu_shop_icon/medium/public/7f37444b0a6a0e2.jpg
https://img1.doubanio.com/spic/s29544798.jpg
https://img3.doubanio.com/icon/g83759-2.jpg
https://img1.doubanio.com/spic/s29637917.jpg
https://img3.doubanio.com/dae/niffler/niffler/images/c4972ec0-e3bf-11e7-9d88-0242ac110021.jpg
https://img1.doubanio.com/view/photo/albumcover/public/p2505713659.jpg
https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2503997609.jpg
https://img1.doubanio.com/dae/niffler/niffler/images/50d72036-b010-11e7-a539-0242ac110017.png
https://img3.doubanio.com/icon/g109498-1.jpg
https://img3.doubanio.com/view/photo/albumcover/public/p2505456924.jpg
https://img1.doubanio.com/icon/g210869-9.jpg
https://img1.doubanio.com/spic/s29595319.jpg
https://img3.doubanio.com/f/sns/1cad523e614ec4ecb6bf91b054436bb79098a958/pics/sns/anony_home/doubanapp_qrcode.png
https://img3.doubanio.com/pics/new_menu.gif
https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2505778884.jpg
https://img3.doubanio.com/mpic/s29625593.jpg
https://img3.doubanio.com/spic/s29636535.jpg
https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2506466229.jpg
https://img1.doubanio.com/img/songlist/large/40001-8.jpg
https://img1.doubanio.com/spic/s29633198.jpg
https://img3.doubanio.com/view/event_poster/small/public/4f75dd97b556862.jpg
https://img1.doubanio.com/icon/g37688-27.jpg
https://img3.doubanio.com/img/songlist/large/361110-2.jpg
https://img3.doubanio.com/icon/g407193-15.jpg
https://img1.doubanio.com/view/dianpu_product_item/medium/public/p509169.jpg
https://img3.doubanio.com/view/site/small/public/1a88bf5414e0183.jpg
https://img3.doubanio.com/f/shire/a1fdee122b95748d81cee426d717c05b5174fe96/pics/blank.gif
https://img3.doubanio.com/view/dianpu_shop_icon/medium/public/169b1b76356f636.jpg
https://img1.doubanio.com/spic/s29596649.jpg
https://img1.doubanio.com/view/site/small/public/3b499309227835a.jpg
https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2504892832.jpg
https://img3.doubanio.com/icon/g402725-3.jpg
https://img3.doubanio.com/mpic/s29587365.jpg
https://img3.doubanio.com/view/dianpu_shop_icon/medium/public/9d03efbf705887d.jpg
https://img3.doubanio.com/dae/niffler/niffler/images/f9493ac4-d428-11e7-a75c-0242ac11002e.jpg
https://img3.doubanio.com/pics/icon/jubao.png
https://img1.doubanio.com/dae/niffler/niffler/images/8a67026e-ba13-11e7-9f54-0242ac110038.png
https://img3.doubanio.com/img/songlist/large/255390-1.jpg
https://img1.doubanio.com/mpic/s29611548.jpg
https://img3.doubanio.com/icon/g10083-4.jpg
https://img1.doubanio.com/icon/g362263-7.jpg
https://img3.doubanio.com/icon/g33120-3.jpg
https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2507361925.jpg
https://img3.doubanio.com/pics/biaoshi.gif
'''