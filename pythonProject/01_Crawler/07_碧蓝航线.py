# 通用工具类
import CrawlerUtils
import DBUtil
import copy
import time
from datetime import datetime
import platform
import argparse
from lxml import etree

# 数据名称
TABLE_NAME = "AZURLANE"
# DB取得配置信息
result = DBUtil.SearchOne("configration", "BASE_URL,IMG_URL,WAIT_TIME,LIST_URL,LOCAL_DIRECTORY,LINUX_DL_PATH", {"TABLE_NAME": TABLE_NAME})
# 基本URL
BASE_URL = result[0]
# 图片地址
BASE_IMG_URL = result[1]
# 间隔时间
SLEEP_TIME = result[2]
# 一览列表路径
LIST_URL = result[3]
# 下载路径
DL_PATH = result[4] if platform.system() == "Windows" else result[5]
# 已登录数据的最新发布时间
maxDate = datetime.strptime(DBUtil.SearchOne(TABLE_NAME, "IFNULL(max(RELEASE_DATE),'2000-01-01')", {})[0], "%Y-%m-%d")
# 结果输出路径
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\AZURLUNE\\"
# 单独爬取
FILTER_NAMES = ["New_Jersey"]
# 中途开始
BREAK_POINT = 0
# 下载flag
DL_FLAG = False
# 从DB下载图片flag
DLIMG_FROM_DB = False
# 覆盖flag
OVERWRITE_FLAG = False
# 数据模型
DATA_MODEL = {
    "ID" : "" # 主键
    , "NAME" : "" # 英文名
    , "NAME_CN" : "" # 中文名
    , "NAME_JP" : "" # 日文名
    , "IMG_NAME" : "" # 立绘图片文件夹名
    , "FACE_IMG" : "" # 头像
    , "RARITY" : "" # 稀有度
    , "CLASSIFICATION" : "" # 舰船类型
    , "FACTION" : "" # 阵营
    , "SKIN_LIST" : [] # 皮肤列表
    , "SKIN_NAME" : [] # 皮肤名
    , "SPRITE_IMG_LIST" : [] # 战斗小人
    , "ARTWORKS" : [] # 艺术集
    , "CONSTRUCTION" : "" # 建造时间
    , "SKILLS" : [] # 技能
    , "SKILL_ICON" : [] # 技能图标
}

# 数据List
DATA_LIST = []
# Master数据
MASTER_DATA = {
  'RARITY': {} # 稀有度
  , 'CLASSIFICATION': {} # 舰船类型
  , 'FACTION': {} # 阵营
}

# excute
def main():
    try:
        getDateList()
    except Exception as e:
        DBUtil.closeConnection()
        print("发生错误!")
        print(e)
    # 更新master信息
    DBUtil.updateCrawlerMaster(MASTER_DATA)
    # 关闭数据库连接
    DBUtil.closeConnection()
    print("End")

def getDateList():
    '''
    从一览取得数据集合
    '''
    # Step.1 发送请求取得DOM对象
    listDoc = CrawlerUtils.getDomFromUrlByCondition(LIST_URL, "div", {"id": "mw-content-text"}, "list.html")

    # Step.2 使用正则匹配
    pattern = (r'<tr><td data-sort-value="(?P<ID>.*?)"><a href="/wiki/(?P<IMG_NAME>.*?)" title="(?P<NAME>.*?)">.*?</a></td><td><a.*?>.*?</a></td>'
           r'<td.*?>(?P<RARITY>.*?)</td><td.*?><a.*?>(?P<CLASSIFICATION>.*?)</a></td><td><a.*?>(?P<FACTION>.*?)</a></td>'
           r'<td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td></tr>')
    dataList = CrawlerUtils.getDataListByReg(str(listDoc), pattern)
    print(f"一览数据总数:{len(dataList)}")

    for index, listData in enumerate(dataList):
        # 初始化数据
        data = CrawlerUtils.initData(DATA_MODEL, listData)
        # 筛选条件
        filterKey = data["IMG_NAME"]
        # 是否爬取当前数据flag
        detailFlag = False

        # 不进行条件筛选
        if len(FILTER_NAMES) == 0 or FILTER_NAMES[0] == "" :
            # 自定义筛选条件
            print(f"进度:{index+1} / {len(dataList)} : {filterKey}")
            if index+1 >= BREAK_POINT :
                detailFlag = True
        elif filterKey in FILTER_NAMES:
            print(f"进度:{FILTER_NAMES.index(filterKey)+1} / {len(FILTER_NAMES)} : {filterKey}")
            detailFlag = True
        
        # Step.3 取得详细内容
        if detailFlag:
            getDetail(data)
            DATA_LIST.append(data)
            # Step.5 爬虫间隔时间,不要不间断请求
            DBUtil.doInsertOrUpdate(TABLE_NAME, data, {'ID': data['ID']})
            print(f"rest {SLEEP_TIME} second")
            time.sleep(SLEEP_TIME)
        

def getDetail(data):
    '''
    取得单个详细情报
    '''
    detailDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + data["IMG_NAME"], "div", {"id": "mw-content-text"}, "detail.html")
    soup = detailDoc.find("div", attrs={"class":"ship-card eagle-union-plate"})
    # 解析具体情报
    headline = soup.find("div", attrs={"class":"card-headline"})
    # 头像
    data["FACE_IMG"] = CrawlerUtils.getSrcFromImgElement(soup.select_one('.shipgirl-image img'))[0:4]
    # 阵营
    factionIcon = CrawlerUtils.getSrcFromImgElement(soup.select_one('.card-logo img'))
    masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'FACTION', 'CATEGORY_NAME': '阵营', 'CODE':data["FACTION"] , 'IMG_URL': factionIcon}
    DBUtil.editMasterData(MASTER_DATA, "FACTION", data["FACTION"], masterData)
    names = headline.find_all("span")
    if len(names) >= 2 :
        # 中文名
        data["NAME_CN"] = headline.find_all("span")[1].text.strip()   
        # 日文名
        data["NAME_JP"] = headline.find_all("span")[2].text.strip()
    # 稀有度
    masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'RARITY', 'CATEGORY_NAME': '稀有度', 'CODE':data["RARITY"] , 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "RARITY", data["RARITY"], masterData)
    # 建造时间
    data["CONSTRUCTION"] = soup.find("td").text.strip()
    # 舰船类型
    shipIcon = CrawlerUtils.getSrcFromImgElement(soup.select_one('.card-class-stamp img'))
    masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'CLASSIFICATION', 'CATEGORY_NAME': '舰船类型', 'CODE':data["CLASSIFICATION"] , 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "CLASSIFICATION", data["CLASSIFICATION"], masterData)
    # 技能
    skillDoc = detailDoc.find("table", attrs={"class":"ship-skills wikitable"})
    for rowEle in skillDoc.find_all("tr")[1:4]:
        # 提取技能图标的 URL 
        icon_url = CrawlerUtils.getSrcFromImgElement(rowEle.find('td', class_='skill-icon').find('img'))
        # 提取中文技能名 
        cn_name = rowEle.find('span', lang='zh').text.strip()
        data["SKILLS"].append(cn_name)
        # 技能图标
        data["SKILL_ICON"].append(icon_url)
    CrawlerUtils.printJson(data)
    return
    # 皮肤列表
    skinDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + data["IMG_NAME"] + "/Gallery", "div", {"id": "mw-content-text"}, "gallery.html")
    for skinEle in skinDoc.find_all("section", attrs={"class":"tabber__section"}):
        # 皮肤图片
        default_panel = soup.find('article', id=lambda x: x and 'Default' in x)
        default_img = default_panel.find('img')['src'] if default_panel else None
        without_bg_panel = soup.find('article', id=lambda x: x and 'Without_BG' in x)
        without_bg_img = without_bg_panel.find('img')['src'] if without_bg_panel else None
        skinImg = CrawlerUtils.getSrcFromImgElement(skinEle.find("img"))
        data["SKIN_LIST"].append(skinImg)
        # 皮肤名
        skinName = skinEle.find("h3").text.strip().replace("/","")
        data["SKIN_NAME"].append(skinName)
        #  

    # 战斗小人
    data["SPRITE_IMG_LIST"] = ""
    # 艺术集
    data["ARTWORKS"] = ""


if __name__ == "__main__":
    print("==> 碧蓝航线爬虫开始")
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="爬取{碧蓝航线}数据")
    parser.add_argument("-n", "--names", default="", help="英文名,多个使用逗号分隔")
    parser.add_argument("-dl", "--download", default="False", help="下载文件开关")
    parser.add_argument("-db", "--databaseDL", default="False", help="下载DB中登录但未下载开关")
    parser.add_argument("-p", "--breakpoint", default="0", help="中途开始点")
    arges = parser.parse_args()
    if arges.names != "":
        FILTER_NAMES = arges.names.split(",")
    if arges.download.lower() == "true":
        DL_FLAG = True
    if arges.databaseDL.lower() == "true":
        DLIMG_FROM_DB = True
    BREAK_POINT = int(arges.breakpoint)
    print(f"过滤名称:{FILTER_NAMES},下载图片:{DL_FLAG},中途开始点:{BREAK_POINT},从DB下载图片:{DLIMG_FROM_DB}")
    main()
