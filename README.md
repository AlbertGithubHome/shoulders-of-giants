[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/AlbertGithubHome/shoulders-of-giants/releases/tag/v0.1.0)
[![License](https://img.shields.io/badge/license-GPL3.0-blue.svg)](https://github.com/AlbertGithubHome/shoulders-of-giants/blob/master/LICENSE)

# shoulders-of-giants
the project will provide some demos and I hope them to be shoulders of giants.

## I. mysql_udf_demo

1. 主要呈现一个使用Mysql UDF的示例，UDF全称是user defined function
2. UDF属于mysql的一个拓展接口，一般翻译为用户自定义函数，这个是用来拓展mysql的技术手段
3. 目前只实现了windows平台的C++版本，也就是mysql调用dll中的扩展函数
4. 后续有时间会增加linux版本，和其他语言版本


## II. web_crawler_demo

1. 主要做一个简单爬虫方法的整理，其中包括对网页、图片、数据的爬取
2. 对于每种资源的爬取都提供了一些demo，方便日后随取随用，不需要做太多变换

### simple_images_crawler
- 对网页内图片资源的简单爬取
- 可用于下载一组好看的背景图，而不用一个个手动点击图片另存为

### website_htmls_crawler
- 对网站页面的简单爬取，可以通过匹配目录内容，下载整个教程信息
- 包含伪装浏览器爬取和伪装多个浏览器爬取，防止爬取失败
- 该示例一开始可以爬取完整教程，但后来网站可能升级了，爬取部分内容提示失败，以后有时间升级代码

### image_crawler_with_chinese_url
- 对图片路径包含中文的图片成功爬取
- 图片路径如果包含中文，正确转码是关键，有疑问时可以回头来看看

### advanced_crawler_game
- 这是由黑板客提供的一个爬虫游戏，由浅入深，真的挺有趣
- 此demo提供了这个爬虫游戏的1-5关解法，后续网站如果更新，此项目会继续跟进
- 玩游戏的过程中还可以提升自己的爬虫技能，做出这样的网站真的很有意义
- 在此对作者表示感谢，并且附上链接地址：[黑板客爬虫](http://www.heibanke.com/lesson/crawler_ex00/)


## III. image_recognition_demo

1. 这个demo源于爬取网站时对验证码的识别，进而可以扩展到对图片文字的识别
2. 此demo目前只有python代码版本，主要提供两种识别方式，分别是通过tesseract识别和百度API识别
3. tesseract识别需要安装tesseract软件，并且引入pytesseract库即可
4. 百度API识别分为直接访问api链接识别、引入百度图片识别库然后创建识别客户端来进行识别
5. 后续有时间继续尝试其他的识别方式，以及通过其他语言来编写识别图片代码