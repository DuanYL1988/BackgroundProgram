'''
碧蓝航线数据爬取
'''
from lxml import etree
from bs4 import BeautifulSoup
import CrawlerUtils

# 全局变量定义
# 基本域名
BASE_URL = "https://azurlane.koumakan.jp/"
# 一览页面URL
LIST_URL = "wiki/List_of_Ships"
# 图片基本域名
BASE_IMG_SRC = "https://azurlane.netojuu.com/images/"
# 基本名
BASE_NAME = {"en":"azurlane","cn":"碧蓝航线","jp":"アズールレーン"}
# 访问间隔
SLEEP_TIME = 30
# 数据集合
MODEL_LIST = []

''' 实际处理 '''
# 1. 取得一览html并使用xpath加载
html = etree.HTML(CrawlerUtils.doGetText(BASE_URL + LIST_URL))
# 2. 取得列表元素
modelList = []
for row in html.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr'):
    if len(row.xpath('./td[1]/a/text()')) > 0:
        model = {} 
        model["no"] = row.xpath('./td[1]/a/text()')[0]
        model["name"] = row.xpath('./td[1]/a/@title')[0]
        model["link"] = row.xpath('./td[1]/a/@href')[0]
        model["countryCd"] = row.xpath('./td[5]/a/@href')[0]
        # 详细页面
        detailHtml = etree.HTML(CrawlerUtils.doGetText(BASE_URL + model["link"]))
        detail = detailHtml.xpath('//*[@id="mw-content-text"]/div[1]/div[2]/div/div[1]/div')
        model["faceImg"] = detail.xpath('./div[1]//img/@src')[0].strip(BASE_IMG_SRC)
        model["nameCn"] =  detail.xpath('./div[2]/div[3]/span[2]/text()')
        model["nameJp"] =  detail.xpath('./div[2]/div[3]/span[3]/text()')
        # 立绘页面
        galleryHtml = BeautifulSoup(CrawlerUtils.doGetText(BASE_URL + model["link"] + "/Gallery"), "html.parser")
        
        modelList.append(model)

'''
# 2.1 扩展功能取得中文名
htmlCn = etree.HTML(CrawlerUtils.doGetText("https://wiki.biligame.com/blhx/%E8%88%B0%E8%88%B9%E5%9B%BE%E9%89%B4"))
modelListCn = []
for item in htmlCn.xpath('//*[@id="CardSelectTr"]'):
    model = {} 
    model["shipType"] = item.xpath('./div/@data-param1')[0].split(",")[-1]
    model["rarity"] = item.xpath('./div/@data-param2')[0]
    model["country"] = item.xpath('./div/@data-param3')[0]
    model["nameCn"] = item.xpath('./div/div/div/a/@title')[0]
    link = item.xpath('./div/div/div/a/@href')[0]
    # 详细页面
    detailHtml = etree.HTML(CrawlerUtils.doGetText("https://wiki.biligame.com/" + link))
    detail = detailHtml.xpath('//*[@id="mw-content-text"]/div/div[10]/div[1]/table[1]/tbody')
    model["no"] = detail.xpath('./tr[2]/td[3]/span/text()')
    modelListCn.append(model)
'''


