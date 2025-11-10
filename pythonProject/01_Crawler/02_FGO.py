# 通用工具类
import CrawlerUtils
import DBUtil
import copy
import time
from datetime import datetime

# 数据名称
TABLE_NAME = "FGO_SERVANT"
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
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\FGO_SERVANT\\"
# 单独爬取
FILTER_NAMES = [""]
# 中途开始
BREAK_POINT = 182
# 下载flag
DL_FLAG = True
# 覆盖flag
OVERWRITE_FLAG = False
# 数据模型
DATA_MODEL = {
    "ID" : "" # ID
    , "NAME" : "" # 英文名
    , "NAME_CN" : "" # 中文名
    , "NAME_JP" : "" # 日文名
    , "IMG_NAME" : "" # 立绘图片文件夹名
    , "CLASS_TYPE" : "" # 职介
    , "RARITY" : "" # 稀有度
    , "HERO_TYPE" : "" # 从者类型(拐,打手)
    , "GENDER" : "" # 性别
    , "ATTRS" : "" # 属性
    , "SUB_ATTRS" : "" # 副属性
    , "TRAITS" : "" # 特性
    , "HP" : "" # 生命值
    , "ATTACT" : "" # 攻击
    , "EVENT_FLAG" : "" # 活动从者
    , "SKILL_1" : "" # 1技能
    , "SKILL_2" : "" # 2技能
    , "SKILL_3" : "" # 3技能
    , "SKILL_EXTRA" : "" # 宝具名
    , "EXTRA_TYPE" : "" # 宝具类型(单体,全体)
    , "EXTRA_COLOR" : "" # 宝具颜色
    , "FACE_IMG" : "" # 头像URL
    , "DEFAULT_STAGE" : "" # 默认状态
    , "STAGE_IMG" : [] # 普通立绘
    , "SKIN_IMG" : [] # 灵衣立绘
    , "STAGE_NAME_LIST" : [] # 状态名集合
    , "SPRITE_IMG" : [] # 地图人物图片
    , "ICON_IMG" : [] # 头像图标立绘
    , "FORMATION_IMG" : [] # 组队立绘
    , "PORTRAITS_IMG" : [] # 对话框立绘
    , "EXPRESSION_SHEETS" : [] # 表情集
    , "CRAFT_ESSENCES" : [] # 相关礼装
    , "ARTWORKS" : [] # 艺术集
    , "ILLUSTRATIONS" : [] # 立绘集
    , "EMOJI" : [] # 表情包
    , "HERO_RANK" : "" # 评价等级
    , "PICK_FLAG" : "" # 抽中flag
    , "RELEASE_DATE" : "" # 登录日期
}

# 数据List
DATA_LIST = []
# Master数据
MASTER_DATA = {
  'CLASS_TYPE': {} # 职介
  , 'ATTRS': {} # 属性
  , 'TRAITS': {} # 特性
}

'''
从一览取得数据集合
'''
def getDateList(listUrl, rarity):
    # Step.1 发送请求取得DOM对象
    listDoc = CrawlerUtils.getDomFromUrlByCondition(listUrl, "table", {"class": "wikitable"}, "list.html")

    # Step.2 使用正则匹配
    dataList = listDoc.find_all("span", attrs={"class":"servant_icon"})
    for index, detailEle in enumerate(dataList):
        sevantName = detailEle.find("a").get("href").replace("/wiki/","")
        # 初始化数据
        data = copy.deepcopy(DATA_MODEL)
        data["NAME"] = sevantName.split("_(")[0].strip()
        data["IMG_NAME"] = sevantName
        data["RARITY"] = rarity
        # 头像URL
        data["FACE_IMG"] = CrawlerUtils.getSrcFromImgElement(detailEle.find("img"))
        data["ID"] = data["FACE_IMG"][5:9]
        # 筛选条件
        filterKey = data["NAME"].replace("_"," ")
        # 是否爬取当前数据flag
        detailFlag = False

        # 不进行条件筛选
        if len(FILTER_NAMES) == 0 or FILTER_NAMES[0] == "" :
            # 自定义筛选条件
            print(f"进度:{index+1} / {len(dataList)} : {sevantName}")
            if index+1 >= BREAK_POINT :
                detailFlag = True
        elif filterKey in FILTER_NAMES:
            print(f"进度:{FILTER_NAMES.index(filterKey)+1} / {len(FILTER_NAMES)} : {filterKey}")
            detailFlag = True

        # Step.3 取得详细内容
        if detailFlag:
            getDetail(data, sevantName)
            # Step.5 爬虫间隔时间,不要不间断请求
            print(f"rest {SLEEP_TIME} second")
            time.sleep(SLEEP_TIME)
        #return

'''
取得单个详细情报
'''
def getDetail(data, urlName):
    detailDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + urlName, "div", {"class": "mw-content-ltr mw-parser-output"}, "detail.html")
    # 解析基本情报
    baseInfoDoc = detailDoc.find("div",{"class": "ServantInfoWrapper"})
    # 日文名
    infoTrs = baseInfoDoc.find_all("tr")
    data["NAME_JP"] = infoTrs[0].find("span",attrs={"lang":"jp"}).text
    data["NAME_JP"] = data["NAME_JP"].split(";")[0].strip()
    # 职介
    classEle = baseInfoDoc.find("div",attrs={"class":"ServantInfoClass"})
    classText = classEle.find("a").get("title")
    data["CLASS_TYPE"] = classText
    masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'CLASS_TYPE', 'CATEGORY_NAME': '职介', 'CODE': classText, 'NAME': classText, 'IMG_URL': CrawlerUtils.getSrcFromImgElement(classEle.find("img"))}
    DBUtil.editMasterData(MASTER_DATA, "CLASS_TYPE", classText, masterData)
    # 立绘
    for imgEle in baseInfoDoc.find_all("div",attrs={"class","wds-tab__content"}):
        title = imgEle.find("a").get("title")
        imgSrc = CrawlerUtils.getSrcFromImgElement(imgEle.find("img"))
        # 普通立绘
        if "Stage" in title:
            data["STAGE_IMG"].append(imgSrc);
        elif "Sprite" in title:
            # 地图人物图片
            data["SPRITE_IMG"].append(imgSrc);
        else:
            # 灵衣图片
            data["SKIN_IMG"].append(imgSrc);
    # 从者类型(拐,打手)
    data["HERO_TYPE"] = ""
    # 性别
    data["GENDER"] = infoTrs[11].find("a").text
    # 属性
    attrs = ""
    for tdEle in infoTrs[7].find("td").find_all("a"):
        attr = tdEle.text
        if "Attribute" != attr:
            attrs = attrs + "," + attr
            masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'ATTRS', 'CATEGORY_NAME': '属性', 'CODE': attr, 'IMG_URL': ''}
            DBUtil.editMasterData(MASTER_DATA, "ATTRS", attr, masterData)
    data["ATTRS"] = attrs[1:]
    # 副属性
    data["SUB_ATTR"] = ""
    # 特性
    traits = ""
    for tdEle in infoTrs[12].find_all("a"):
        trait = tdEle.text
        if "Traits" != trait:
            traits = traits + "," + trait
            masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'TRAITS', 'CATEGORY_NAME': '特性', 'CODE': trait, 'IMG_URL': ''}
            DBUtil.editMasterData(MASTER_DATA, "TRAITS", trait, masterData)
    data["TRAITS"] = traits[1:]
    # 生命值
    hpAtkTr = infoTrs[3].find_all("td")
    if data["ID"] not in ["S154"]:
        hpTd = CrawlerUtils.matchHp(hpAtkTr[0].text)
        if "/" not in hpTd:
            hpAtkTr = infoTrs[2].find_all("td")
            hpTd = CrawlerUtils.matchHp(hpAtkTr[0].text)
        data["HP"] = hpTd.split("/")[1]
        # 攻击
        atkTd = CrawlerUtils.matchHp(hpAtkTr[1].text)
        data["ATTACT"] = atkTd.split("/")[1]
    # 活动从者
    data["EVENT_FLAG"] = ""
    # 主动技能
    SkillDoc = getSkillDocWithName(detailDoc,"Active_Skills")
    divList = SkillDoc.find_all("div",attrs={"class","wds-tab__content"})
    if len(divList) == 3:
        # 1技能
        data["SKILL_1"] = getSkillTxt(divList[0])
        data["SKILL_2"] = getSkillTxt(divList[1])
        data["SKILL_3"] = getSkillTxt(divList[2])
    else:
        # 1技能 data["ID"] not in ["S037"]
        data["SKILL_1"] = getSkillTxt(SkillDoc)
        # 2技能
        skill2Doc = SkillDoc.find_next_sibling()
        data["SKILL_2"] = getSkillTxt(skill2Doc)
        # 3技能
        skill3Doc = skill2Doc.find_next_sibling()
        data["SKILL_3"] = getSkillTxt(skill3Doc)
    # 宝具名
    extraEle = getSkillDocWithName(detailDoc,"Noble_Phantasm")
    tableEles = extraEle.find("caption")
    capDivList = tableEles.find_all("div",attrs={"class","wds-tab__content"})
    if len(capDivList) > 0:
        tableEles = capDivList[-1]
    data["SKILL_EXTRA"] = tableEles.text.strip()
    # 宝具颜色
    imgEle = extraEle.find("img")
    data["EXTRA_COLOR"] = imgEle.get("data-image-key").split(".")[0]
    # 宝具类型(单体,全体)
    data["EXTRA_TYPE"] = ""

    # 各种图片下载
    galleryDoc = CrawlerUtils.getDomFromUrlByCondition(f"{BASE_URL}Sub:{urlName}/Gallery" , "div", {"id": "mw-content-text"}, "gallery.html")
    # 头像图标立绘
    for imgObj in getImagesWithBorChildId(galleryDoc, "Servant_Icons"):
        if "IconRaw" in imgObj["src"]:
            data["ICON_IMG"].append(imgObj["src"])
    # Portraits
    for imgObj in getImagesWithBorChildId(galleryDoc, "Portraits"):
        data["PORTRAITS_IMG"].append(imgObj["src"])
    # 组队立绘 Formations
    for imgObj in getImagesWithBorChildId(galleryDoc, "Formations"):
        data["FORMATION_IMG"].append(imgObj["src"])
    # TODO 表情集
    data["EXPRESSION_SHEETS"] = []
    # 相关礼装
    for imgObj in getImagesWithBorChildId(galleryDoc, "Craft_Essences"):
        data["CRAFT_ESSENCES"].append(imgObj["src"])
    # 艺术集 Story_Artworks
    for imgObj in getImagesWithBorChildId(galleryDoc, "Story_Artworks"):
        data["ARTWORKS"].append(imgObj["src"])
    # 立绘集
    for imgObj in getImagesWithBorChildId(galleryDoc, "Illustrations"):
        data["ILLUSTRATIONS"].append(imgObj["src"])
    # 表情包
    for imgObj in getImagesWithBorChildId(galleryDoc, "Other_Media"):
        if "LINE" in imgObj["name"]:
            data["EMOJI"].append(imgObj["src"])
    # 登录日期
    data["RELEASE_DATE"] = ""
    DBUtil.doInsertOrUpdate(TABLE_NAME, data, {"ID" : data["ID"]})
    if DL_FLAG:
        editDownlaodImgInfo(data)

def getSkillDocWithName(htmlDoc, elementId):
    extraEle = htmlDoc.find(attrs={"id":elementId}).parent
    extraEle = extraEle.find_next_sibling()
    return extraEle.find("div",attrs={"class":"wds-tab__content wds-is-current"})

def getSkillTxt(htmlDoc):
    skillEle = htmlDoc.find_all("table")[-1]
    skillEle = skillEle.find_all("td")[1]
    wpDivList = skillEle.find_all("div",attrs={"class","wds-tab__content"})
    if len(wpDivList) > 0 :
        return wpDivList[0].text.strip()
    else:
        return skillEle.text.strip()

def getImagesWithBorChildId(htmlDoc,elementId):
    imgList = []
    try:
        targetEle = htmlDoc.find(id=elementId)
        titleEle = targetEle.parent
        galleryDiv = titleEle.find_next_sibling()
        imgEleList = galleryDiv.find_all("div", attrs={"class":"wikia-gallery-item"})
        for imgDiv in imgEleList:
            imgEle = imgDiv.find("img")
            imgList.append({"name":imgEle.get("alt"),"src":CrawlerUtils.getSrcFromImgElement(imgEle)})
        return imgList
    except Exception as e:
        print("该ID取得图片出错")
        return imgList

def editDownlaodImgInfo(detailData):
    dlImgList = []
    # Stage
    for stageindex in range(0,4,1) :
        imgUrl = detailData["STAGE_IMG"][stageindex];
        name = imgUrl.split('/')[-1].split('.')[0]
        imgObj = {"url":BASE_IMG_URL + imgUrl
            ,"path":detailData["ID"] + "_" + detailData["IMG_NAME"] + "/"
            ,"name":name}
        # dlImgList.append(imgObj)
    # Emoji
    for emoji in detailData["EMOJI"]:
        imgUrl = emoji;
        name = imgUrl.split('/')[-1].split('.')[0]
        imgObj = {"url":BASE_IMG_URL + imgUrl
            ,"path":"09_emoji/"
            ,"name": name}
        dlImgList.append(imgObj)
    # 礼装
    for emoji in detailData["CRAFT_ESSENCES"]:
        imgUrl = emoji;
        name = imgUrl.split('/')[-1].split('.')[0]
        imgObj = {"url":BASE_IMG_URL + imgUrl
            ,"path":"01_CraftEssences/"
            ,"name": name}
        # dlImgList.append(imgObj)

    for imgObj in dlImgList:
        CrawlerUtils.downloadImage(DL_PATH + imgObj["path"],imgObj["name"],imgObj["url"],OVERWRITE_FLAG, False)

# 爬取数据
for rarity in range(5, 4, -1):
    listUrl = LIST_URL.replace("{key}", str(rarity))
    getDateList(listUrl,rarity)
    # CrawlerUtils.printJson(MASTER_DATA)

# 更新master信息
#DBUtil.updateCrawlerMaster(MASTER_DATA)

# 关闭数据库连接
DBUtil.closeConnection()
print("End")
