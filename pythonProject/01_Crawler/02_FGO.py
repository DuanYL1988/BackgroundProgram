'''
一览内容区分种别表示时,可以使用多进程来实现
使用线程池
'''
# 线程池
from concurrent.futures import ThreadPoolExecutor
# 通用工具类
import CrawlerUtils

# 职介种类
CLASS_LIST = ["Saber","Archer","Lancer","Rider","Caster","Assassin","Berserker","Ruler"
             ,"Alter Ego","Foreigner","Pretender","Shielder","Beast","Moon Cancer","Avenger"]
# 基本URL
BASE_URL = "https://fategrandorder.fandom.com/wiki/"
# 数据集合
MODEL_LIST = []

def getDataByClass(classType):
    print(classType,"START")
    html = CrawlerUtils.doGetText(BASE_URL + classType)
    xpath = '//*[@id="mw-content-text"]/div/table[3]/tbody/tr/td'
    rows = CrawlerUtils.getXpathForHtml(html, xpath)
    count = 0
    for tdEle in rows:
        if len(tdEle.xpath('./a/@href')) > 0 :
            count = count + 1
            model = {}
            model["link"] = tdEle.xpath('./a/@href')[0]
            model["name"] = tdEle.xpath('./a/@title')[0]
            MODEL_LIST.append(model)
    print(classType,"END",count)

"""
for classType in CLASS_LIST:
    getDataByClass(classType)
print(MODEL_LIST)
""" 
 
if __name__ == "__main__":
    with ThreadPoolExecutor(len(CLASS_LIST)) as t:
        for classType in CLASS_LIST:
            t.submit(getDataByClass,classType=classType)
    # 等待线程全部结束后执行(守护)
    print(len(MODEL_LIST))
