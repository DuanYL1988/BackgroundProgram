# 通用工具类
from datetime import datetime
import argparse
import copy
import time
import re
import json
import os
import platform
import CrawlerUtils
import DBUtil

# 数据名称
TABLE_NAME = "FIREEMBLEM_HERO"
# 基本URL
print("==> 取得DB配置信息")
result = DBUtil.SearchOne("configration", "base_url,img_url,wait_time,list_url,LOCAL_DIRECTORY,LINUX_DL_PATH", {"TABLE_NAME": TABLE_NAME})
BASE_URL = result[0]
BASE_IMG_URL = result[1]
SLEEP_TIME = result[2]
LIST_URL = result[3]
LOCAL_DIRECTORY = result[4] if platform.system() == "Windows" else result[5]
# 已登录数据的最新发布时间
maxDate = datetime.strptime(DBUtil.SearchOne(TABLE_NAME, "IFNULL(max(RELEASE_DATE), '2015-01-01')", {})[0], "%Y-%m-%d")
# 中途开始
BREAK_POINT = 0
# 数据集合
MODEL_LIST = []
# 单独爬取 "Lyn:_Brave_Lady"
FILTER_NAMES = []
# 图片下载Flag
DOWNLOAD_FLAG = True
# 覆盖flag
OVERWRITE_FLAG = False
# 读取DB中未下载图片的数据进行下载
DLIMG_FROM_DB = False
# 数据模型
DATA_MODEL = {
    "ID" : "" # 主键ID
    , "TITLE_NAME" : "" # 称号
    , "NAME" : "" # 名
    , "NAME_CN" : "" # 中文名
    , "NAME_JP" : "" # 日文名
    , "IMG_NAME" : "" # 立绘名
    , "FACE_IMG" : "" # 头像
    , "STAGE_IMG" : [] # 状态立绘
    , "CUT_IN_IMG" : [] # 插入立绘
    , "SPRITE_IMG" : [] # 地图人物图片
    , "ART_IMG" : [] # 关联立绘
    , "RARITY" : [] # 稀有度
    , "HP" : "" # 生命
    , "ATK" : "" # 攻击
    , "SPD" : "" # 速度
    , "DEF" : "" # 防御
    , "RES" : "" # 魔防
    , "BLESSING" : "" # 祝福
    , "HERO_TYPE" : "" # 类型
    , "MOVE_TYPE" : "" # 兵种
    , "WEAPON" : "" # 武器名
    , "WEAPON_TYPE" : "" # 武器类型
    , "WEAPON_POWER" : "" # 武器攻击力
    , "ENTRY" : "" # 角色作品
    , "COLOR" : "" # 宝珠颜色
    , "RACE" : "" # 种族
    , "SKILL_A" : "" # A技能
    , "SKILL_B" : "" # B技能
    , "SKILL_C" : "" # C技能
    , "SKILL_ASS" : "" # 辅助技能
    , "SKILL_SP" : "" # 必杀技
    , "LIMIT_PLUS" : "" # 突破极限
    , "DRAGON_FLOWER" : "" # 神龙之花
    , "FAVORITE" : "" # 喜欢
    , "HERO_RANK" : "" # 评价等级
    , "PICK_FLAG" : "" # 抽中flag
    , "RELEASE_DATE" : "" # 登录日期
}
# 数据List
DATA_LIST = []
# Master数据
CODE_MODEL = {
    "APPLICATION" : TABLE_NAME,
    "CATEGORY_ID" : "",
    "CATEGORY_NAME" : "",
    "CODE" : "",
    "IMG_URL" : ""
}
CODE_DIRT = {}
# 武器技能表
SKILL_TABLE = "FIREEMBLEM_HERO_SKILL"
SkillCdModel = {
    "SKILL_CATEGORY" : "" # 技能类型
    , "SKILL_CODE" : "" # 技能Code
    , "SKILL_NAME_CN" : "" # 中文名
    , "SKILL_NAME_JP" : "" # 日文名
    , "SKILL_ICON" : "" # 技能图标/武器图片
    , "DESCRPTION" : "" # 技能描述
    , "SKILL_RANGE" : "" # 技能范围
    , "SKILL_COLD_DOWN" : "" # 冷却回合
    , "WEAPON_MIGHT" : "" # 武器威力
    , "SKILL_EFFECT" : "" # 技能特效
    , "SKILL_COST" : "" # 技能花费
}

# 定义映射关系
HERO_TYPE_MAP = {
    "Attuned": "响心",
    "Emblem": "纹章士",
    "Duo": "连翼",
    "SpecialDuo": "连翼",
    "Rearmed": "魔器",
    "Legendary": "传承",
    "Harmonized": "双界",
    "Mythic": "神階",
    "Ascended": "開花"
}

def main():
    CrawlerUtils.setRequetHeaders({"Referer": "https://feheroes.fandom.com/"})
    if DLIMG_FROM_DB:
        # 读取DB中未下载图片的数据进行下载
        getUnDownloadData()
    else:
        getDateList(LIST_URL)
    # 关闭数据库连接
    DBUtil.closeConnection()
    print("==> 火焰纹章英豪 爬虫结束")

def getUnDownloadData():
    '''
    取得未下载图片的数据
    '''
    cnt,total,updCnt = 0, 0, 0
    updateQuery = f"UPDATE {TABLE_NAME} SET FAVORITE = 'DownloadED' WHERE IMG_NAME IN ('TEST_UPDATE_CONDTION'"
    for row in DBUtil.doSearchQuery(f"SELECT IMG_NAME, FACE_IMG, STAGE_IMG, CUT_IN_IMG, SPRITE_IMG, ART_IMG, NAME FROM {TABLE_NAME} WHERE FAVORITE is null"):
        dlPath = LOCAL_DIRECTORY + row[0]
        # 未下载且满足条件
        if os.path.exists(dlPath) == False and row[6] in FILTER_NAMES:
            cnt += 1
            print(f'CNT:{cnt}/{total} , dlPath: {dlPath}')
            downloadFehImgFromDB(row)
            updateQuery += f",'{row[0].replace("'","''")}'"
    # 最后更新剩余的
    updateQuery += ")"
    DBUtil.doExcuteQuery(updateQuery)

def getDateList(listUrl):
    """
    方法体要写在主处理之前
    根据html结构使用合适的解析方式
    通过id,class可以特定1个可以使用dom方式解析
    """
    listDoc = CrawlerUtils.getDomFromUrl(listUrl, "list.html")
    # Step.2 从一览中解析
    tableTrArr = listDoc.find_all("tr", attrs={"class": "hero-filter-element"})
    # Step.3 取得详细内容
    for index, trElement in enumerate(tableTrArr):
        detailUrl = trElement.find_all("a")[0].get("title")
        # Step.2-1 单独取得数据     print("run here")
        if len(FILTER_NAMES) > 0 and "" != FILTER_NAMES[0]:
            detailUrl = detailUrl.replace(" ","_")
            if detailUrl in FILTER_NAMES:
                print(detailUrl)
                DATA_LIST.append(getDetail(detailUrl))
        # 从条件中取得
        else:
            print(f"进度:{index+1} / {len(tableTrArr)} : {detailUrl}")
            # 中途开始
            if  index+2 > BREAK_POINT:
                DATA_LIST.append(getDetail(detailUrl))
    # 4. 持久化数据
    # ExcelUtils.writeData(TABLE_NAME, DATA_LIST, CodeList)

def getDetail(detailUrl):
    # 初始化数据
    data = copy.copy(DATA_MODEL)
    # 根据URL参数设置情报
    data["NAME"] = detailUrl.split(":")[0]
    data["IMG_NAME"] = detailUrl.replace(":", "").replace(" ", "_")
    data["LIMIT_PLUS"] = 0
    data["DRAGON_FLOWER"] = 0

    detailHtml = CrawlerUtils.getDomFromUrl(BASE_URL + detailUrl, "detail.html")
    #detailHtml = TestUtil.getFeheroDetail(BASE_URL + detailUrl, "detail.html")
    # 头像
    imgKey = detailUrl.replace(":", "").replace(" ", "_").replace("'","") + "_Face_FC.webp"
    faceImgEle = detailHtml.find("img", attrs={"data-image-key": imgKey})
    if faceImgEle is None:
        print(f"当前imgKey关键字没找到匹配元素{imgKey},{detailUrl}")  
        return
    # {imgName}_Face_FC.webp
    data["FACE_IMG"] = CrawlerUtils.getSrcFromImgElement(faceImgEle)[0:5]

    # 立绘
    detailDoc = detailHtml.find("div", {"class": "mw-parser-output"})
    baseInfoDiv = detailDoc.find("div", {"class": "hero-infobox"})
    baseInfoTable = baseInfoDiv.find("table", {"class": "wikitable"})
    imgDivs = baseInfoTable.find_all("a", {"class": "image"})
    data["STAGE_IMG"] = []
    for element in imgDivs:
        data["STAGE_IMG"].append(CrawlerUtils.getSrcFromImgElement(element.find("img"))[0:5])
    # 基本信息
    for thElement in baseInfoTable.find_all("td"):
        title = thElement.text
        # 稀有度
        if "Rarities" in title:
            rarity = thElement.find_next_sibling().text
            rarity = rarity.replace("\xa0","")
            rarity = rarity.replace("\n","")
            rarity = rarity.replace(" ","")
            rarity = rarity.replace('Focus—','')
            data["RARITY"] = rarity[0:1]
            data["PICK_FLAG"] = "1" if "5" == rarity else "0" if "3" == rarity else ""
            if rarity[0:1] == "3" or rarity[0:1] == "2":
                print(f"太辣鸡了不登录{rarity}")
                deleteData(data["IMG_NAME"])
                return
            # 英雄类型(响心,魔器,...)
            heroTypeName = HERO_TYPE_MAP[rarity[1:]]
            if heroTypeName is not None:
                data["HERO_TYPE"] = rarity
                masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'HERO_TYPE', 'CATEGORY_NAME': '英雄类型', 'CODE': rarity, 'NAME': heroTypeName, 'IMG_URL': ''}
                # DBUtil.editMasterData(MASTER_DATA, "HERO_TYPE", classText, masterData)
        # 实装时间
        elif "Release Date" in title  :
            data["RELEASE_DATE"] = thElement.find_next_sibling().find("time").text
            releaseDate = datetime.strptime(data["RELEASE_DATE"], "%Y-%m-%d")
            # 不是单独爬取的话,已登录最大时间之前数据不解析
            if releaseDate < maxDate and (len(FILTER_NAMES) == 0 or ""==FILTER_NAMES[0]):
                print("发布时间点已登录")
                return
        # 武器类型
        elif "Weapon" in title :
            weaponInfo = thElement.find_next_sibling().find("img").get("data-image-key").split("_")
            data["COLOR"] = weaponInfo[2]
            weaponType = weaponInfo[3].split(".")[0]
            data["WEAPON_TYPE"] = thElement.find_next_sibling().find("a").get("title")
            data["RACE"] = "Dragon" if "Breath" == weaponType else "Beast" if "Beast" == weaponType else "Human"
        # 移动类型
        elif "Move" in title :
            data["MOVE_TYPE"] = thElement.find_next_sibling().find("a").get("title")
        # 作品
        elif "Entry" in title :
            data["ENTRY"] = thElement.find_next_sibling().find_all("a")[-1].get("title").replace("Fire Emblem: ","").replace("Fire Emblem ","")
        elif "Internal ID" in title and "Enemy" not in title :
            # 使用正则匹配数字
            InternalId = thElement.find_next_sibling().text
            data["ID"] = CrawlerUtils.matchStr(InternalId, r".*?\((\d+)\)")
            # 通过InternalId[PID_xxx(id)]来获取类型
            heroType = CrawlerUtils.matchStr(InternalId, r"_(.*?)\(")
            if "" == data["HERO_TYPE"]:
                #text = heroType.replace(nameJp[1], "")
                match = re.search(r'PID_(.*?) \(', InternalId)
                if match:
                    text = match.group(1)
                    text = re.sub(r'[\u30A0-\u30FF]+', '', text)
                    data["HERO_TYPE"] = text
    if "" != data["HERO_TYPE"]:
        print(data["ID"])
        DBUtil.doUpdate(TABLE_NAME,{"HERO_TYPE":data["HERO_TYPE"]},{"IMG_NAME" : data["IMG_NAME"]})

    # 基础数值
    statusTds = detailDoc.find(id="Level_40_stats").find_parent().find_next_sibling().select("table > tbody > tr > td")[-6 :-1]
    data["HP"] = statusTds[0].text.split("/")[-1]
    data["ATK"] = statusTds[1].text.split("/")[-1]
    data["SPD"] = statusTds[2].text.split("/")[-1]
    data["DEF"] = statusTds[3].text.split("/")[-1]
    data["RES"] = statusTds[4].text.split("/")[-1]
    # 武器
    weaponTable = getParentNextElementById(detailDoc, "Weapons")
    if weaponTable is None:
        weaponTable = getParentNextElementById(detailDoc, "Ally_Weapons")
        if weaponTable is None:
            weaponTable = getParentNextElementById(detailDoc, "Enemy_Weapons")
    weaponTds = weaponTable.select("table > tbody > tr > td")[-7: -1]
    # 武器英文名
    weaponCd = weaponTds[0].find("a").get("title")
    data["WEAPON"] = weaponCd
    data["WEAPON_POWER"] = weaponTds[1].text
    # 武器字典
    weaponObj = copy.deepcopy(SkillCdModel)
    weaponObj["SKILL_CATEGORY"] = "FE_WEAPON"
    weaponObj["SKILL_CODE"] = weaponCd
    weaponObj["WEAPON_MIGHT"] = weaponTds[1].text
    weaponObj["DESCRPTION"] = weaponTds[3].text
    skillDirt = {"FE_WEAPON": weaponObj, "FE_SKILL_A": None, "FE_SKILL_B": None, "FE_SKILL_C": None, "FE_SKILL_ASS": None, "FE_SKILL_SP": None}
    # 技能
    # 辅助技能
    assistsTds = getParentNextElementById(detailDoc, "Assists").find_all("td")
    if assistsTds is not None and len(assistsTds) > 0:
        skillObj = copy.deepcopy(SkillCdModel)
        assist = assistsTds[-6].text
        skillObj["SKILL_CATEGORY"] = "FE_SKILL_ASS"
        skillObj["SKILL_CODE"] = assist
        skillObj["DESCRPTION"] = assistsTds[-4].text
        skillDirt["FE_SKILL_ASS"] = skillObj
    # 必杀技
    specialsTds = getParentNextElementById(detailDoc, "Specials").find_all("td")
    if specialsTds is not None and len(specialsTds) > 0:
        skillObj = copy.deepcopy(SkillCdModel)
        specials = specialsTds[-6].text
        skillObj["SKILL_CATEGORY"] = "FE_SKILL_SP"
        skillObj["SKILL_CODE"] = specials
        skillObj["DESCRPTION"] = specialsTds[-4].text
        skillDirt["FE_SKILL_SP"] = skillObj
    # 技能A-C
    skillTrs = getParentNextElementById(detailDoc, "Passives").find_all("tr")
    index = 1
    while index < len(skillTrs):
        # 第一行标题,跳过
        thEle = skillTrs[index].find("th")
        if thEle is not None:
            levelMax = (index - 1) + int(thEle.get("rowspan"))
            levelMaxRow = skillTrs[levelMax].find_all("td")
            skillABC = thEle.text
            skillObj = copy.deepcopy(SkillCdModel)
            skillObj["SKILL_CATEGORY"] = "FE_SKILL_" + skillABC
            skillObj["SKILL_CODE"] = levelMaxRow[1].find("a").get("title")
            skillObj["SKILL_ICON"] = CrawlerUtils.getSrcFromImgElement(levelMaxRow[0].find("img"))
            skillObj["DESCRPTION"] = levelMaxRow[2].text
            skillDirt["FE_SKILL_"+skillABC] = skillObj
        index = index + 1
    data["SKILL_A"] = "" if skillDirt["FE_SKILL_A"] is None else skillDirt["FE_SKILL_A"]["SKILL_CODE"]
    data["SKILL_B"] = "" if skillDirt["FE_SKILL_B"] is None else skillDirt["FE_SKILL_B"]["SKILL_CODE"]
    data["SKILL_C"] = "" if skillDirt["FE_SKILL_C"] is None else skillDirt["FE_SKILL_C"]["SKILL_CODE"]
    data["SKILL_ASS"] = "" if skillDirt["FE_SKILL_ASS"] is None else skillDirt["FE_SKILL_ASS"]["SKILL_CODE"]
    data["SKILL_SP"] = "" if skillDirt["FE_SKILL_SP"] is None else skillDirt["FE_SKILL_SP"]["SKILL_CODE"]
    # 解析武器,技能详细信息
    getWeaponSkillInfo(skillDirt, data["RACE"])

    # 取得MISC情报
    getDetailMisc(data, detailUrl)

    # 是否已经登录过
    condition = {"IMG_NAME" : data["IMG_NAME"]}
    existFlag = DBUtil.getCount(table=TABLE_NAME, condition = condition)

    # DB登录
    try:
        DBUtil.doInsertOrUpdate(TABLE_NAME, data, {"ID" : data["ID"]})
    except Exception as e:
        print(e)
        print("DB更新发生异常:", data["IMG_NAME"])
    
    # 下载图片
    if DOWNLOAD_FLAG:
        print("开始下载图片:" + data["IMG_NAME"])
        downloadFehImgFromDB([data["IMG_NAME"], data["FACE_IMG"], data["STAGE_IMG"], data["CUT_IN_IMG"], data["SPRITE_IMG"], data["ART_IMG"], data["NAME"]])
    # 休息5秒
    print("rest 5 second")
    time.sleep(SLEEP_TIME)

def getWeaponSkillInfo(skillDirtMap, race):
    # 单个英雄技能组
    for skillType in skillDirtMap:
        # 技能分类
        skillData = skillDirtMap[skillType]
        # 有该技能时
        if skillData is not None :
            skillCd = skillData["SKILL_CODE"]
            unionKey = {"SKILL_CATEGORY" : skillType, "SKILL_CODE": skillCd}
            # 验证DB中是否已经存在
            existCnt = DBUtil.getCount(SKILL_TABLE, unionKey)
            # if existCnt == 0 :
            # 解析情报并登录
            skillDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + skillCd, "div", {"id": "mw-content-text"}, "error.html")
            #skillDoc = TestUtil.getFeheroDetailByCond(BASE_URL + skillCd, "div", {"id": "mw-content-text"}, "error.html")
            langInfo = getLanguage(skillDoc)
            # TODO 可能会发生错误
            if langInfo is not None:
                skillData["SKILL_NAME_CN"] = langInfo["cn"]
                skillData["SKILL_NAME_JP"] = langInfo["jp"]
            # 图片
            if skillType == "FE_WEAPON" and ("Dragon,Beast".find(race) < 0):
                # 去除Code中特殊字符
                keyword = CrawlerUtils.matchWeapon("Weapon " + skillCd)
                imgElement = skillDoc.find("img", attrs={"alt": keyword})
                # 无法通过关键字找到时
                if imgElement is None:
                    divEle = skillDoc.find_all("table", attrs={"class": "wikitable default ibox"}) # 
                    if divEle is not None and len(divEle) > 0:
                        imgElement = divEle.select("a > img")[0]
                        skillData["SKILL_ICON"] = CrawlerUtils.getSrcFromImgElement(imgElement)
            elif skillType == "FE_SKILL_A" or skillType == "FE_SKILL_B" or skillType == "FE_SKILL_C":
                skillData["SKILL_ICON"] = skillDirtMap[skillType]["SKILL_ICON"]
            DBUtil.doInsertOrUpdate(SKILL_TABLE, skillData, unionKey)

def getDetailMisc(data, detailUrl):
    '''
    取得MISC情报
    '''
    # Misc
    detailMisc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + detailUrl + "/Misc", "div", {"class": "mw-parser-output"}, "detail2.html")
    #detailMisc = TestUtil.getFeheroDetailByCond(BASE_URL + detailUrl + "/Misc", "div", {"class": "mw-parser-output"}, "detail2.html")
    # 称号
    titleLang = getLanguage(detailMisc)
    if " " in titleLang["cn"]:
        data["TITLE_NAME"] = titleLang["cn"].split(" ")[0]
        data["NAME_CN"] = titleLang["cn"].split(" ")[1]
    elif "\u3000" in titleLang["cn"]:
        data["TITLE_NAME"] = titleLang["cn"].split("\u3000")[0]
        data["NAME_CN"] = titleLang["cn"].split("\u3000")[1]
    # 日文称号
    if "\u3000" in titleLang["jp"]:
        nameJp = titleLang["jp"].split("\u3000")
        data["NAME_JP"] = nameJp[1]

    # TODO 解析异常
    # CutIn
    cutInImgBox = getImagesFromSpanTitle(detailMisc, "Gallery")
    # 初始化
    data["CUT_IN_IMG"] = []
    data["ART_IMG"] = []
    data["SPRITE_IMG"] = []
    for imgElement in cutInImgBox:
        imgSrc = CrawlerUtils.getSrcFromImgElement(imgElement)
        if "BtlFace_BU" in imgSrc:
            # {imgName}_BtlFace_BU.webp,BU_D.webp(_Resplendent_BtlFace_BU.webp)
            data["CUT_IN_IMG"].append(imgSrc[0:5])
        elif "Artist_" in imgSrc:
            data["ART_IMG"].append(imgSrc)
    # Sprite
    spriteImgBox = getImagesFromSpanTitle(detailMisc, "Sprite")
    if spriteImgBox is None:
        spriteImgBox = getImagesFromSpanTitle(detailMisc, "Sprites")
    for imgElement in spriteImgBox:
        imgSrc = CrawlerUtils.getSrcFromImgElement(imgElement)
        #print(f"Sprite:{imgSrc}")
        if "Mini_Unit" in imgSrc:
            # {IMG_NAME}{"_Mini_Unit_"}XX.png
            data["SPRITE_IMG"].append(imgSrc.replace(data["IMG_NAME"],"").replace("_Mini_Unit_",""))

    # 解析异常
    if len(data["CUT_IN_IMG"]) > 2:
        # data["CUT_IN_IMG"] = "exception:" + str(len(data["CUT_IN_IMG"]))
        data["CUT_IN_IMG"] = "[]"
    print(data["SPRITE_IMG"])
    if len(data["SPRITE_IMG"]) > 20:
        # data["CUT_IN_IMG"] = "exception:" + str(len(data["CUT_IN_IMG"]))
        data["SPRITE_IMG"] = "[]"
    return

def getLanguage(doc):
    '''
    多语言取得
    '''
    langDirt = {"cn" :"", "jp": ""}
    langElement = getParentNextElementById(doc, "In_other_languages")
    # TODO
    if langElement is None:
        return
    if langElement.find("span", {"lang": "zh-Hant-TW"}) is not None:
        langDirt["cn"] = langElement.find("span", {"lang": "zh-Hant-TW"}).text
    if langElement.find("span", {"lang": "ja"}) is not None:
        langDirt["jp"] = langElement.find("span", {"lang": "ja"}).text
    return langDirt

def getImagesFromSpanTitle(doc, SpanId):
    '''
    取得图片Gallery元素群
    '''
    galleryElement = getParentNextElementById(doc, SpanId)
    imgBox = []
    if galleryElement is not None:
        for imgElement in galleryElement.find_all("img"):
            imgBox.append(imgElement)
    return imgBox

def getParentNextElementById(doc, elementId):
    """
    通过Span标题取得对应的内容
    """
    spanElement = doc.find(id=elementId)
    if spanElement is None:
        spanElement = doc.find(id=f"Ally_{elementId}")
        if spanElement is None:
            spanElement = doc.find(id="Enemy_" +elementId)
    try:
        infoElement = spanElement.find_parent().find_next_sibling()
        return infoElement
    except Exception as e:
        print("取得Span对应下一个元素失败:", elementId)  
        return None

def getCodeListFromListPage(listUrl):
    '''
    解析的html一个元素内包含多个需要的内容时可以使用正规方式进行一次性解析
    '''
    listDoc = CrawlerUtils.doGetText(listUrl)
    parttenStr = (r'<tr class="hero-filter-element" data-move-type="(?P<moveType>.*?)".*?data-weapon-type="(?P<weaponType>.*?)" data-weapon-props=".*?'
                  r'<td>.*?</td><td.*?</td><td.*?<img alt="(?P<entry>.*?)" src=".*?images/(?P<entryIcon>.*?).png.*?</td>'
                  r'<td.*?src=".*?images/(?P<moveIcon>.*?).png.*?</td>'
                  r'<td.*?src=".*?images/(?P<weaponIcon>.*?).png.*?</td>'
                  r'.*?</tr>')
    dataList = CrawlerUtils.getDataListByReg(listDoc, parttenStr)
    for data in dataList:
        # 武器
        weaponCode = copy.deepcopy(CODE_MODEL)
        weaponCode["CATEGORY_ID"] = "WEAPON_TYPE"
        weaponCode["CATEGORY_NAME"] = "武器种类"
        weaponCode["CODE"] = data["weaponType"]
        weaponCode["IMG_URL"] = data["weaponIcon"]+".png"
        CODE_DIRT.update({data["weaponType"]: weaponCode})
        # 移动
        moveCode = copy.deepcopy(CODE_MODEL)
        moveCode["CATEGORY_ID"] = "MOVE_TYPE"
        moveCode["CATEGORY_NAME"] = "移动方式"
        moveCode["CODE"] = data["moveType"]
        moveCode["IMG_URL"] = data["moveIcon"]+".png"
        CODE_DIRT.update({data["moveType"]: moveCode})
        # 作品
        entryCode = copy.deepcopy(CODE_MODEL)
        entryCode["CATEGORY_ID"] = "ENTRY"
        entryCode["CATEGORY_NAME"] = "作品"
        entryCode["CODE"] = data["entry"]
        entryCode["IMG_URL"] = data["entryIcon"]+".png"
        CODE_DIRT.update({data["entry"]: entryCode})
    codeList = []
    for key in CODE_DIRT:
        codeList.append(CODE_DIRT[key])
        DBUtil.doInsertOrUpdate("CODE_MASTER", CODE_DIRT[key],{"application": TABLE_NAME, "CATEGORY_ID": CODE_DIRT[key]["CATEGORY_ID"], "CODE": CODE_DIRT[key]["CODE"]})

def deleteData(imgName):
    DBUtil.doDelete(TABLE_NAME,{"IMG_NAME":imgName})

def downloadFehImgFromDB(result):
    """ 爬虫执行完后从DB读取数据下载图片 """
    imgHost = [BASE_IMG_URL,result[0]]
    targetPath = LOCAL_DIRECTORY + result[0] + "\\"
    dataModel = {
        "faceImg": {"src": f"{BASE_IMG_URL}{result[1]}{result[0]}_Face_FC.webp", "name" : "00_face"}
    }
    stageImgsDirt = ["_Face.webp","_BtlFace.webp","_BtlFace_C.webp","_BtlFace_D.webp"]
    fileNames = ["01_normal","02_attact","03_extra","04_break"]
    editListImg(dataModel, "stage", imgHost, result[2], stageImgsDirt, fileNames)
    cutInImgDirt = ["_BtlFace_BU.webp","_BtlFace_BU_D.webp"]
    fileNames = ["11_cutIn_att","12_cutIn_dmg"]
    for imgData in dataModel["stage"]:
        CrawlerUtils.downloadImage(targetPath, imgData["name"], imgData["src"], False, True)
    editListImg(dataModel, "cutIn", imgHost, result[3], cutInImgDirt, fileNames)
    spriteImgDirt = []
    spriteSrc = []
    print(result)
    # 还没有cutin的时候
    for src in transToList(result[4]):
        netSrc = f"{src[:5]}{result[0]}_Mini_Unit_{src[5:]}"
        spriteSrc.append(netSrc)
        spriteImgDirt.append(f"Mini_Unit_{src[5:]}")
    # TODO 图片url转换后规则未解析
    #editListImg(dataModel, "sprite", imgHost, result[4],spriteSrc, spriteImgDirt)

    print(CrawlerUtils.formateJSON(dataModel))
    CrawlerUtils.downloadImage(targetPath, dataModel["faceImg"]["name"], dataModel["faceImg"]["src"], False, True)
    for imgData in dataModel["cutIn"]:
        CrawlerUtils.downloadImage(targetPath, imgData["name"], imgData["src"], False, True)

def editListImg(dataModel, attrNm, imgHost, imgNameStr, srcMpNames, fileNames):
    dataModel[attrNm] = [] # 初始化
    imgSrcList = transToList(imgNameStr)
    if len(imgSrcList) > 0:
        if ("[" in imgNameStr and "]" in imgNameStr):
            imgSrcList = json.loads(imgNameStr)
        else:
            imgSrcList = imgNameStr
        if len(imgSrcList) > 0:
            for index,stageSrc in enumerate(imgSrcList):
                # 神装英雄
                if(index > len(fileNames)-1):
                    return
                mpName = srcMpNames[index] if len(srcMpNames) > index else ""
                skinIndex = index
                skinName = ""
                if index > 3:
                    skinIndex = skinIndex - 4
                    skinName = f"{fileNames[skinIndex]}(new)"
                else:
                    skinName = f"{fileNames[skinIndex]}"
                dataModel[attrNm].append({
                   "src": f"{imgHost[0]}{stageSrc}{imgHost[1]}{mpName}"
                   , "name": skinName
                })

def transToList(strList):
    '''
    将字符串格式的List转换为List格式
    '''
    if isinstance(strList, list):
        return strList
    if strList is None or strList == "":
        return []
    try:
        return json.loads(strList)
    except:
        return []

if __name__ == "__main__":
    print("==> 火焰纹章英豪 爬虫开始")
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="爬取火焰纹章英豪数据")
    parser.add_argument("-n", "--names", default="", help="英文名,多个使用逗号分隔")
    parser.add_argument("-dl", "--download", default="False", help="下载文件开关")
    parser.add_argument("-db", "--databaseDL", default="False", help="下载DB中登录但未下载开关")
    parser.add_argument("-p", "--breakpoint", default="0", help="中途开始点")
    # 解析参数
    arges = parser.parse_args()
    if arges.names != "":
        FILTER_NAMES = arges.names.split(",")
    if arges.download.lower() == "true":
        DOWNLOAD_FLAG = True
    if arges.databaseDL.lower() == "true":
        DLIMG_FROM_DB = True
    BREAK_POINT = int(arges.breakpoint)
    # FILTER_NAMES = ["Gullveig:_Hidden_in_Time"]
    print(f"过滤名称:{FILTER_NAMES},下载图片:{DOWNLOAD_FLAG},中途开始点:{BREAK_POINT},从DB下载图片:{DLIMG_FROM_DB}")
    main()