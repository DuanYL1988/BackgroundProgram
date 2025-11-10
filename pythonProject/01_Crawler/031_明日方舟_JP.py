# 通用工具类
import CrawlerUtils
import DBUtil

# 数据名称
TABLE_NAME = "ARKNIGHTS_OPERATOR_JP"
# 基本URL
result = DBUtil.SearchOne("configration", "base_url,img_url,wait_time,list_url,LOCAL_DIRECTORY", {"table_name": TABLE_NAME})
BASE_URL = result[0]
BASE_IMG_URL = result[1]
SLEEP_TIME = result[2]
DL_PATH = result[4]

# 数据集合
MODEL_LIST = []
# 单独爬取 "ケストレル"
FILTER_NAMES = [""]
# 执行断点
BREAK_POINT = 385
# 覆盖flag
OVERWRITE_FLAG = False
# 数据模型
DATA_MODEL = {
    "NAME" : "" # 英文名
    , "NAME_CN" : "" # 中文名
    , "NAME_JP" : "" # 日文名
    , "SKIN_ICON" : "" # 头像
    , "SKIN_SPRITE" : "" # 精1立绘
    , "SPRITE_IMG" : "" # 地图人物图片
}

# 数据List
DATA_LIST = []

def getDateList(listUrl):
    print(listUrl)
    listDoc = CrawlerUtils.getDomFromUrlByCondition(listUrl, "div", {"id": "body"}, "list.html")
    # Step.2 使用正则匹配
    pattern = (r'<td class="style_td" style="background-color:.*?"><a class="" data-mtime="" href=".*?" title="(?P<NAME_JP>.*?)">.*?<img alt=".*?" class="lazyload" data-src=".*?</a></td>')
    dataList = CrawlerUtils.getDataListByReg(str(listDoc), pattern)
    breakFlag = True
    for index, listData in enumerate(dataList):
        data = CrawlerUtils.initData(DATA_MODEL, listData) 
        filterKey = data["NAME_JP"]
        if index+1 >= BREAK_POINT:
            breakFlag = False
        if breakFlag and ""!=BREAK_POINT : continue
        print(f"进度:{index+1} / {len(dataList)} : {filterKey}")
        getDetail(data)
  
def getDetail(data):
    print(data["NAME_JP"])
    detailDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + "?" + data["NAME_JP"], "div", {"id": "body"}, "detail.html")
    baseInfoTable = detailDoc.find("h2",attrs={"id":"content_1_0"}).find_next_sibling().find("table")
    baseInfoRows = baseInfoTable.find_all("td")
    # 地图人物图片
    data["SPRITE_IMG"] = CrawlerUtils.getSrcFromImgElement(baseInfoTable.find_all("img")[1]).replace("attach2/","")
    # 稀有度
    rarityInt = int(baseInfoRows[2].text[1:])
    if rarityInt < 3: 
        print("稀有度不满足条件,结束处理")
        return
    # 皮肤
    loopStartFlag = True
    skinStart = 2
    while loopStartFlag:
        skinStart = skinStart + 1
        # 循环到达上限
        if skinStart == 25:
            loopStartFlag = False
        picId = "content_1_" + str(skinStart + rarityInt)
        h2Ele = detailDoc.find("h2",attrs={"id":picId})
        if h2Ele is None:
            continue
        # 满足条件
        if "コーデ" in h2Ele.text:
            picDiv = h2Ele.find_next_sibling()
            while "div" != picDiv.name:
                picDiv = picDiv.find_next_sibling()
            index = 0
            while "rgn-container" in picDiv.get("class"):
                if index > 0:
                    trsEle = picDiv.find_all("tr")[3]
                    tds = trsEle.find_all("td")
                    if len(tds) >= 2 and tds[1].find("img") is not None:
                        iconSrc = CrawlerUtils.getSrcFromImgElement(tds[0].find("img")).replace("attach2/","")
                        splitSrc = CrawlerUtils.getSrcFromImgElement(tds[1].find("img")).replace("attach2/","")
                        data["SKIN_ICON"] += iconSrc + ","
                        data["SKIN_SPRITE"] += splitSrc + ","
                index += 1
                picDiv = picDiv.find_next_sibling()
            if "" != data["SKIN_ICON"]:
                data["SKIN_ICON"] = data["SKIN_ICON"][:-1]
                data["SKIN_SPRITE"] = data["SKIN_SPRITE"][:-1]
        if "小ネタ" in h2Ele.text:
            #                                              "英語名: "
            nameStr = h2Ele.find_next_sibling().text.split("英語名：")
            nameStr = nameStr if len(nameStr) == 2 else nameStr[0].split("英語名:")
            if len(nameStr) >= 2:
                data["NAME_CN"] = nameStr[0].replace("中国語名：","").replace("中国語名:","").split("　")[0].split(" ")[0].strip().replace("・","·")
                data["NAME"] = nameStr[1].split("\n")[0].strip()
    condition = {"NAME_CN": data["NAME_CN"], "NAME_JP": "null"}
    if DBUtil.getCount("ARKNIGHTS_OPERATOR", condition) == 1:
        DBUtil.doUpdate("ARKNIGHTS_OPERATOR",data,condition)

# 没有指定条件时,全取得
if len(FILTER_NAMES) > 0 and FILTER_NAMES[0] != "":
    for keyWord in FILTER_NAMES:
        data = CrawlerUtils.initData(DATA_MODEL, {"NAME_JP": keyWord}) 
        getDetail(data)
        print(CrawlerUtils.formateJSON(data))
else:    
    getDateList(result[3])
# 关闭数据库连接 维娜·维多利亚
DBUtil.closeConnection()
print("End")
