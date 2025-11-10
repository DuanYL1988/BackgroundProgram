# 通用工具类
import CrawlerUtils
import DBUtil
import time
from datetime import datetime

# 数据名称
TABLE_NAME = "WUTHERING_WAVE_RESONATOR"
# DB取得配置信息
result = DBUtil.SearchOne("configration", "BASE_URL,IMG_URL,WAIT_TIME,LIST_URL,LOCAL_DIRECTORY", {"table_name": TABLE_NAME})
# 已登录数据的最新发布时间
maxDate = datetime.strptime("2000-01-01", "%Y-%m-%d")
maxDateQuery = DBUtil.SearchOne(TABLE_NAME, "max(RELEASE_DATE)", {})
if maxDateQuery[0] is not None:
    maxDate = datetime.strptime(DBUtil.SearchOne(TABLE_NAME, "max(RELEASE_DATE)", {})[0], "%Y-%m-%d")
# 基本URL
BASE_URL = result[0]
# 图片地址
BASE_IMG_URL = result[1]
# 间隔时间
SLEEP_TIME = result[2]
# 一览列表路径
LIST_URL = result[3]
# 下载路径
DL_PATH = result[4]
# 结果输出路径
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\WUTHERING_WAVE_RESONATOR\\"
# 单独爬取 Cartethyia
FILTER_NAMES = [""]
# 中途开始
BREAK_POINT = 0
# 下载flag
DL_FLAG = False
# 覆盖flag
OVERWRITE_FLAG = False
# 数据模型
DATA_MODEL = {
    "ID" : "" # 主键
    , "NAME" : "" # 英文名
    , "NAME_CN" : "" # 中文名
    , "NAME_JP" : "" # 日文名
    , "FACE_IMG" : "" # 头像
    , "CARD_IMG" : "" # 卡片立绘
    , "SPRITE_IMG" : "" # 编队立绘
    , "POST_IMG" : "" # 海报立绘
    , "RARITY" : "" # 稀有度
    , "ATTRS" : "" # 属性
    , "WEAPON_TYPE" : "" # 武器属性
    , "TAGS" : "" # 词缀
    , "INFLUENCE" : "" # 势力
    , "BIRTH_PLACE" : "" # 出生地
    , "HP" : "" # 生命
    , "ATK" : "" # 攻击
    , "DEF" : "" # 防御
    , "SKILLS" : [] # 技能
    , "SKILLS_ICON" : [] # 技能图标
    , "EMOJI" : [] # 表情包
    , "RELEASE_DATE" : "" # 实装日期
    , "VERSION" : "" # 版本信息
}

# 数据List
DATA_LIST = []
# Master数据
MASTER_DATA = {
  'ATTRS': {} # 属性
  , 'WEAPON_TYPE': {} # 武器属性
}

'''
从一览取得数据集合
'''
def getDateList(listUrl):
    # Step.1 发送请求取得DOM对象
    listDoc = CrawlerUtils.getDomFromUrlByCondition(listUrl, "table", {}, "list.html")

    # Step.2 使用正则匹配
    pattern = (r'<td>.*?<center><span.*? href="/wiki/(?P<NAME>.*?)".*? data-src="https://static.wikia.nocookie.net/wutheringwaves/images(?P<FACE_IMG>.*?)/revision.*?</center>.*?</td>.*?'
               r'<td>.*?<span.*?<span title="(?P<RARITY>.*?) Stars">.*?</td>.*?<td>.*?<span.*?<a href="/wiki/(?P<ATTRS>.*?)" title.*?<img.*?</td>.*?'
               r'<td>.*?<span.*?<a href="/wiki/(?P<WEAPON_TYPE>.*?)" title.*?<img.*?</td>'
               r'.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>.*?<a href="/wiki/Version/(?P<VERSION>.*?)" title.*?</td>')
    dataList = CrawlerUtils.getDataListByReg(str(listDoc), pattern)

    for index, listData in enumerate(dataList):
        # 初始化数据
        data = CrawlerUtils.initData(DATA_MODEL, listData)
        # 筛选条件
        filterKey = data["NAME"]
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

        # 跳过
        if "Rover-" in filterKey:
            detailFlag = False
            continue
        
        # Step.3 取得详细内容
        if detailFlag:
            getDetail(data)
            CrawlerUtils.printJson(data)
            DBUtil.doInsertOrUpdate(TABLE_NAME,data,{"NAME":data["NAME"]})
            DATA_LIST.append(data)
            # Step.5 爬虫间隔时间,不要不间断请求
            print(f"rest {SLEEP_TIME} second")
            time.sleep(SLEEP_TIME)

'''
取得单个详细情报
'''
def getDetail(data):
    detailDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + data["NAME"], "div", {"id": "mw-content-text"}, "detail.html")
    # 解析具体情报
    # 中文名 
    nameTbl = getSkillDocWithName(detailDoc,"Other_Languages")
    cnTr = nameTbl.find_all("tr")[2]
    cnTd = cnTr.find_all("td")[1]
    data["NAME_CN"] = cnTd.text
    # 日文名
    cnTr = nameTbl.find_all("tr")[4]
    cnTd = cnTr.find_all("td")[1]
    data["NAME_JP"] = cnTd.text
    # 卡片立绘
    imgEle = detailDoc.find("div",attrs={"class":"pi-image-collection wds-tabber"})
    imgList = imgEle.find_all("img")
    data["CARD_IMG"] = CrawlerUtils.getSrcFromImgElement(imgList[0])
    # 编队立绘
    data["SPRITE_IMG"] = CrawlerUtils.getSrcFromImgElement(imgList[1])
    # 海报立绘
    if len(imgList) > 2:
        data["POST_IMG"] = CrawlerUtils.getSrcFromImgElement(imgList[2])
    # 
    tdEle = detailDoc.find("td",attrs={"data-source":"attribute"})
    attrImg = CrawlerUtils.getSrcFromImgElement(tdEle.find("img"))
    masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'ATTRS', 'CATEGORY_NAME': '属性', 'CODE': data["ATTRS"], 'IMG_URL': attrImg}
    DBUtil.editMasterData(MASTER_DATA, "ATTRS", data["ATTRS"], masterData)
    tdEle = detailDoc.find("td",attrs={"data-source":"weapon"})
    attrImg = CrawlerUtils.getSrcFromImgElement(tdEle.find("img"))
    masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'WEAPON_TYPE', 'CATEGORY_NAME': '武器类型', 'CODE': data["WEAPON_TYPE"], 'IMG_URL': attrImg}
    DBUtil.editMasterData(MASTER_DATA, "WEAPON_TYPE", data["WEAPON_TYPE"], masterData)
    print(MASTER_DATA)
    # 词缀
    data["TAGS"] = ""
    # 势力
    data["INFLUENCE"] = ""
    # 出生地
    data["BIRTH_PLACE"] = ""
    # 生命
    data["HP"] = ""
    # 攻击
    data["ATK"] = ""
    # 防御
    data["DEF"] = ""
    # 技能
    data["SKILLS"] = ""
    # 技能图标
    data["SKILLS_ICON"] = ""
    # 表情包
    data["EMOJI"] = ""
    # 实装日期
    data["RELEASE_DATE"] = ""

def getSkillDocWithName(htmlDoc, elementId):
    extraEle = htmlDoc.find(attrs={"id":elementId}).parent
    return extraEle.find_next_sibling()


def margeCn():
	TABLE_NAME_CN = "WUTHERING_WAVE_RESONATOR_CN"
	# DB取得配置信息
	resultCn = DBUtil.SearchOne("configration", "BASE_URL,IMG_URL,WAIT_TIME,LIST_URL,LOCAL_DIRECTORY", {"table_name": TABLE_NAME_CN})
	listDoc = CrawlerUtils.getDomFromUrlByCondition(listUrl, "table", {"id":"CardSelectTr"}, "list-CN.html")
	pattern = (r'<tr class="divsort" data-param1="(?P<ATTRS>.*?)" data-param2="5" data-param3="(?P<WEAPON_TYPE>.*?)" data-param4="(?P<TAGS>.*?)">.*?'
			   r'<div class="center"><div class="floatnone"><a href=".*?" title="共鸣者/(?P<NAME_CN>.*?)">.*?</tr>')
	dataList = CrawlerUtils.getDataListByReg(str(listDoc), pattern)
	#
	MASTER_DATA = {'ATTRS':{}, 'WEAPON_TYPE': {}}
	for dataCn in dataList:
		detailUrl = resultCn + dataCn["NAME_CN"]
		detailDoc = CrawlerUtils.getDomFromUrlByCondition(listUrl, "table", {}, "detail-CN.html")
		// TODO
		dbResultCn = DBUtil.SearchOne(TABLE_NAME, "BASE_URL,NAME,NAME_CN,ATTRS,WEAPON_TYPE", {"NAME_CN": dataCn["NAME_CN"]})
		
		masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'ATTRS', 'CATEGORY_NAME': '属性', 'CODE': dbResultCn[2], 'NAME': dataCn[""]}
		DBUtil.editMasterData(MASTER_DATA, "ATTRS", data["ATTRS"], masterData)
		masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'WEAPON_TYPE', 'CATEGORY_NAME': '属性', 'CODE': dbResultCn[3], 'NAME': dataCn[""]}
		DBUtil.editMasterData(MASTER_DATA, "WEAPON_TYPE", data["WEAPON_TYPE"], masterData)
		
		DBUtil.doUpdate(TABLE_NAME,dataCn,{"NAME_CN":data["NAME_CN"]})
		
	DBUtil.updateCrawlerMaster(MASTER_DATA)

# 爬取数据
getDateList(LIST_URL)
#CrawlerUtils.outputJsonCsv(OUTPUT_JSON_PATH,TABLE_NAME,DATA_LIST)

# 更新master信息
DBUtil.updateCrawlerMaster(MASTER_DATA)

# 关闭数据库连接
DBUtil.closeConnection()
print("End")
