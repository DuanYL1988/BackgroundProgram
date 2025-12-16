# 通用工具类
import CrawlerUtils
import DBUtil
import time
import platform

# 数据名称
TABLE_NAME = "ARKNIGHTS_OPERATOR"
# 基本URL
result = DBUtil.SearchOne("configration", "base_url,img_url,wait_time,list_url,LOCAL_DIRECTORY,LINUX_DL_PATH", {"table_name": TABLE_NAME})
# 请求路径
BASE_URL = result[0]
# 图片地址
BASE_IMG_URL = result[1]
# 间隔时间
SLEEP_TIME = result[2]
# 一览列表路径
LIST_URL = result[3]
# 下载路径
DL_PATH = result[4] if platform.system() == "Windows" else result[5]
# 结果输出路径
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\"
# 单独爬取 "海霓","Miss.Christine","露托","海沫","克洛丝","圣聆初雪"
FILTER_NAMES = ["圣聆初雪"]
# 执行断点
BREAK_POINT = 152
# 覆盖flag
OVERWRITE_FLAG = False
# 数据模型
DATA_MODEL = {
    "ID" : "" # 主键
    , "NAME" : "" # 英文名
    , "NAME_CN" : "" # 中文名
    , "NAME_JP" : "" # 日文名
    , "FACE_IMG" : "" # 头像
    , "STAGE_ONE_IMG" : "" # 精1立绘
    , "STAGE_TWO_IMG" : "" # 精2立绘
    , "SPRITE_IMG" : "" # 地图人物图片
    , "SKIN_IMAGE" : "" # 皮肤图片地址
    , "SKIN_NAME" : "" # 皮肤名
    , "DEFALT_SKIN" : "0" # 默认皮肤
    , "RARITY" : "" # 稀有度
    , "VOCATION" : "" # 职业
    , "SUB_VOCATION" : "" # 副职业
    , "TAGS" : "" # 词缀
    , "INFLUENCE" : "" # 势力
    , "BIRTH_PLACE" : "" # 出生地
    , "RACE" : "" # 种族
    , "HP" : "" # 生命
    , "ATK" : "" # 攻击
    , "DEF" : "" # 防御
    , "RES" : "" # 法抗
    , "COST" : "" # 部署费用
    , "SKILLS" : "" # 技能
    , "SKILLS_ICON" : "" # 技能图标
    , "CAPACITY" : "" # 潜能
    , "RELEASE_DATE" : "" # 实装日期 
}
# 数据List
DATA_LIST = []
# Master数据
MASTER_DATA = {
  'VOCATION': {} # 职业
  , 'SUB_VOCATION': {} # 副职业
  , 'INFLUENCE': {} # 势力
  , 'BIRTH_PLACE': {} # 出生地
  , 'RACE': {} # 种族
}

# excute
def main():
    try:
        getDateList()
    except Exception as e:
        print("发生错误!")
        # 更新master信息
        DBUtil.updateCrawlerMaster(MASTER_DATA)
        #CrawlerUtils.outputJsonCsv(OUTPUT_JSON_PATH,TABLE_NAME,DATA_LIST)
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
    listDoc = CrawlerUtils.getDomFromUrlByCondition(LIST_URL, "table", {"id": "CardSelectTr"}, "list.html")

    # Step.2 使用正则匹配
    pattern = (r'<tr class="divsort" data-param1="(?P<VOCATION>.*?)" data-param2="(?P<RARITY>.*?),.*?" data-param3=".*?" data-param4="(?P<INFLUENCE>.*?)" data-param5="(?P<TAGS>.*?)".*?'
               r'<td><div class="role-bg"><div class="center"><div class="floatnone"><a.*?<center><a.*?title="(?P<NAME_CN>.*?)">.*?</td>\n'
               r'<td>.*?</td>\n<td><div class="center">.*?<br/>.*?- (?P<SUB_VOCATION>.*?)\n</td>.*?</tr>')
    dataList = CrawlerUtils.getDataListByReg(str(listDoc), pattern)
    
    # 异常结束时中途开始
    breakFlag = True
    for index, listData in enumerate(dataList):
        # 初始化数据
        data = CrawlerUtils.initData(DATA_MODEL, listData)
        
        # 筛选条件
        filterKey = data["NAME_CN"]
        # 是否爬取当前数据flag
        detailFlag = False
        # 不进行条件筛选
        if len(FILTER_NAMES) == 0 or FILTER_NAMES[0] == "" :
            print(f"进度:{index+1} / {len(dataList)} : {filterKey}")
            # 自定义筛选条件,从断点开始
            if index+1 >= BREAK_POINT and int(data["RARITY"]) > 2:
                detailFlag = True
        else:
            print(filterKey)
            if filterKey in FILTER_NAMES:
                print(f"进度:{FILTER_NAMES.index(filterKey)+1} / {len(FILTER_NAMES)} : {filterKey}")
                detailFlag = True

        # Step.3 取得详细内容
        if detailFlag:
            getDetail(data)
            DATA_LIST.append(data)
            # Step.5 爬虫间隔时间,不要不间断请求
            print(f"rest {SLEEP_TIME} second")
            time.sleep(SLEEP_TIME)

def getDetail(data):
    '''
    取得单个详细情报
    '''
    detailDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + data["NAME_CN"], "div", {"id": "mw-content-text"}, "detail.html")
    # 下载对象集合
    DL_FILE_LIST = []
    # 头像
    faceKey = data["NAME_CN"] + "05.png"
    data["FACE_IMG"] = CrawlerUtils.getSrcFromImgElement(detailDoc.find("img",attrs={"alt": faceKey}))
    DL_FILE_LIST.append({"src":data["FACE_IMG"], "name": "00_face"})
    illDivList = detailDoc.find_all("div",attrs={"class":"switch-tab-content"})
    # 稀有度
    rarityEle = detailDoc.find("div",attrs={"id": "illustrations"}).find_next_sibling()
    data["RARITY"] = rarityEle.find("img").get("alt")[-5:-4]
    rarity = int(data["RARITY"])
    # 精1立绘
    data["STAGE_ONE_IMG"] = CrawlerUtils.getSrcFromImgElement(illDivList[0].find("img"))
    DL_FILE_LIST.append({"src":data["STAGE_ONE_IMG"], "name": "10_stage1"})
    # 立绘
    index = 1
    for illDiv in detailDoc.find_all("div",attrs={"class":"switch-tab operator-page-char-img-type"}):
        if index == 1 and int(data["RARITY"]) > 3:
            # 精2立绘
            data["STAGE_TWO_IMG"] = CrawlerUtils.getSrcFromImgElement(illDivList[index].find("img"))
            DL_FILE_LIST.append({"src":data["STAGE_TWO_IMG"], "name": "10_stage2"})
        else:
            # 皮肤
            skinSrc = CrawlerUtils.getSrcFromImgElement(illDivList[index].find("img"))
            data["SKIN_IMAGE"] += skinSrc + ","
            skinName = illDiv.text.strip().replace("/","")
            data["SKIN_NAME"] += skinName + ","
            DL_FILE_LIST.append({"src":skinSrc, "name": f"20_Skin_{skinName}"})
        index = index + 1
    data["SKIN_IMAGE"] = data["SKIN_IMAGE"][:-1]
    data["SKIN_NAME"] = data["SKIN_NAME"][:-1]
    # 基础信息
    for thEle in detailDoc.find_all("p",attrs={"class": "operator-page-heading-table-th"}):
        # ID
        if "干员编号" == thEle.text:
            data["ID"] = thEle.find_next_sibling().text
        # 职业
        elif "职业" == thEle.text:
            className = thEle.find_next_sibling().text.strip()
            data["VOCATION"] = className
            masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'VOCATION', 'CATEGORY_NAME': '职业', 'CODE': data["VOCATION"], 'IMG_URL': CrawlerUtils.getSrcFromImgElement(thEle.find_next_sibling().find("img"))}
            DBUtil.editMasterData(MASTER_DATA, "VOCATION", data["VOCATION"], masterData)
        # 实装日期
        elif "实装日期" == thEle.text:
            data["RELEASE_DATE"] = CrawlerUtils.matchYMD(thEle.find_next_sibling().text,r'(\d{4})年(\d{1,2})月(\d{1,2})日')
    # 分支
    branchEle = detailDoc.find("div", {"class":"operator-page-section-wrapper flex-container trans-dir-on-xs"})
    branchNm = branchEle.find("span").text.strip()
    data["SUB_VOCATION"] = branchNm
    masterData = {'APPLICATION':TABLE_NAME, 'CATEGORY_ID': 'SUB_VOCATION', 'CATEGORY_NAME': '职业分支', 'CODE': data["SUB_VOCATION"], 'IMG_URL': CrawlerUtils.getSrcFromImgElement(branchEle.find("img"))}
    DBUtil.editMasterData(MASTER_DATA, "SUB_VOCATION", data["SUB_VOCATION"], masterData)
    # 生命
    trEles = detailDoc.find("table", attrs={"class": "full-width operator-basic-stat-table operator-page-section-wrapper"}).find_all("tr")
    rarityTblIndex = 4 if rarity > 3 else 3
    data["HP"] = trEles[1].find_all("td")[rarityTblIndex].text + trEles[1].find_all("td")[rarityTblIndex + 1].text
    # 攻击
    data["ATK"] = trEles[2].find_all("td")[rarityTblIndex].text + trEles[2].find_all("td")[rarityTblIndex + 1].text
    # 防御
    data["DEF"] = trEles[3].find_all("td")[rarityTblIndex].text + trEles[3].find_all("td")[rarityTblIndex + 1].text
    # 法抗
    data["RES"] = trEles[4].find_all("td")[rarityTblIndex].text + trEles[4].find_all("td")[rarityTblIndex + 1].text
    # 种族
    otherInfoEle = detailDoc.find("div",attrs={"class":"operator-page-heading-doc-bg"}).find_all("p")[1].text
    otherInfoDir = CrawlerUtils.splitByReg(otherInfoEle, r'【(.*?)】')
    data["RACE"] = otherInfoDir["种族"]
    # 出生地
    if "出身" in otherInfoDir:
        data["BIRTH_PLACE"] = otherInfoDir["出身"]
    # 天赋
    for capacityDiv in detailDoc.find_all("div", attrs={"class": "talent-table"}):
        data["CAPACITY"] += capacityDiv.find("p").text + ","
    data["CAPACITY"] = data["CAPACITY"][:-1]
    # 技能
    for skillDiv in detailDoc.find("div", attrs={"id": "skill"}).find_all("div", attrs={"class" : "switch-tab"}):
        if skillDiv.find("img") is None:
            skillNm = skillDiv.text.split("]")[-1].strip()
            data["SKILLS"] += skillNm + ","
            skillImg = detailDoc.find("img",attrs={"title":skillNm})
            data["SKILLS_ICON"] += CrawlerUtils.getSrcFromImgElement(skillImg) + ","
        else:
            data["SKILLS"] += skillDiv.text + ","
            data["SKILLS_ICON"] += CrawlerUtils.getSrcFromImgElement(skillDiv.find("img")) + ","
    data["SKILLS"] = data["SKILLS"][:-1]
    data["SKILLS_ICON"] = data["SKILLS_ICON"][:-1]
    # 是否登录DB
    primaryKeys = {"ID":data["ID"]}
    # DB登录
    print(CrawlerUtils.printJson(data))
    try:
        DBUtil.doInsertOrUpdate(TABLE_NAME, data, primaryKeys)
    except Exception as e:
        print("DB更新发生异常:", data["NAME_CN"])    
    # 下载图片
    for dlObj in DL_FILE_LIST:
        CrawlerUtils.downloadImage(DL_PATH+data["NAME_CN"]+"/",dlObj["name"],BASE_IMG_URL + dlObj["src"],False,False)
    print(DL_FILE_LIST)

if __name__ == "__main__":
    main()