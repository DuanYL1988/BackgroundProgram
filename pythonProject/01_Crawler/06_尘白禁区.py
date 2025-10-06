# 通用工具类
import CrawlerUtils
import DBUtil
import time

# 数据名称
TABLE_NAME = "SNOW_BREAK"
# 基本URL
result = DBUtil.SearchOne("configration", "base_url,img_url,wait_time,list_url", {"table_name": TABLE_NAME})
BASE_URL = result[0]
BASE_IMG_URL = result[1]
SLEEP_TIME = result[2]
# 结果输出路径
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\SNOW_BREAK\\"

# 单独爬取
FILTER_NAMES = []
# 执行断点
BREAK_POINT = ""
# 覆盖flag
OVERWRITE_FLAG = False
# 数据模型
DATA_MODEL = {
    "ID" : "" # 主键ID
    , "TITLE_NAME" : "" # 称号
    , "NAME" : "" # 名
    , "IMG_NAME" : "" # 立绘图片文件夹名
    , "FACE_IMG" : "" # 头像
    , "STAGE_IMG" : [] # 状态立绘
    , "RARITY" : "" # 稀有度
    , "HP" : "" # 生命
    , "ATK" : "" # 攻击
    , "DEF" : "" # 防御
    , "ELEMENT_TYPE" : "" # 元素属性
    , "WEAPON_TYPE" : "" # 武器类型
    , "WEAPON" : "" # 武器名
    , "SKIN_NAME" : [] # 皮肤名称
    , "SKIN_IMAGE" : [] # 皮肤立绘
    , "SKIN_SPRITE" : [] # 皮肤战斗图片
    , "FAVORITE" : "" # 喜欢
    , "HERO_RANK" : "" # 评价等级
    , "PICK_FLAG" : "" # 抽中flag
    , "TAGS" : [] # 标签
    , "RELEASE_DATE" : "" # 登录日期
}

# 数据List
DATA_LIST = []
# Master数据
MASTER_DATA = {
  'FE_BLESS': {} # 元素属性
  ,'FE_WEAPON': {} # 武器类型
  ,'FE_RANK': {} # 评价等级
}

'''
从一览取得数据集合
'''
def getDateList(listUrl):
    print(listUrl)
    # Step.1 发送请求取得DOM对象
    listDoc = CrawlerUtils.getDomFromUrlByCondition(listUrl, "div", {"id": "frameRole"}, "list.html")
    # 5星
    for element in listDoc.find_all("div",attrs={"class":"g C5星"}):
        data = CrawlerUtils.initData(DATA_MODEL, {})
        data["TITLE_NAME"] = element.find("div",{"class":"L"}).text
        print(data)
    # 4星

    return

    # Step.2 使用正则匹配
    pattern = (r'<tr class="divsort" data-param1="(?P<VOCATION>.*?)" data-param2="(?P<RARITY>.*?),.*?" data-param3=".*?" data-param4="(?P<INFLUENCE>.*?)" data-param5="(?P<TAGS>.*?)".*?'
               r'<td>.*?</td>\n<td><div class="center">.*?<br/>.*?- (?P<SUB_VOCATION>.*?)\n</td>.*?</tr>')
    dataList = CrawlerUtils.getDataListByReg(str(listDoc), pattern)

    # 异常结束时中途开始
    breakFlag = True
    for index, listData in enumerate(dataList):
        # 初始化数据
        data = CrawlerUtils.initData(DATA_MODEL, listData)
        # 筛选关键字
        filterKey = data["NAME_CN"]
        if filterKey == BREAK_POINT:
            breakFlag = False
        # 从断点开始
        if "" != BREAK_POINT and breakFlag : continue

        print(f"进度:{index+1} / {len(dataList)} : {filterKey}")
        # 自定义筛选条件
        if int(data["RARITY"]) > 2 :
            # Step.3 取得详细内容
            getDetail(data)
            # Step.5 爬虫间隔时间,不要不间断请求
            print(f"rest {SLEEP_TIME} second")
            time.sleep(SLEEP_TIME)

'''
取得单个详细情报
'''
def getDetail(data):
    detailDoc = CrawlerUtils.getDomFromUrlByCondition(BASE_URL + data["NAME"], "div", {"id": "mw-content-text"}, "detail.html")
    # 解析具体情报
    # 主键ID
    data["ID"] = ""
    # 称号
    data["TITLE_NAME"] = ""
    # 名
    data["NAME"] = ""
    # 立绘图片文件夹名
    data["IMG_NAME"] = ""
    # 头像
    data["FACE_IMG"] = ""
    # 状态立绘
    data["STAGE_IMG"] = ""
    # 稀有度
    data["RARITY"] = ""
    # 生命
    data["HP"] = ""
    # 攻击
    data["ATK"] = ""
    # 防御
    data["DEF"] = ""
    # 元素属性
    data["ELEMENT_TYPE"] = ""
    masterData = {'CATEGORY_NAME': '元素属性', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "FE_BLESS", "", masterData)
    # 武器类型
    data["WEAPON_TYPE"] = ""
    masterData = {'CATEGORY_NAME': '武器类型', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "FE_WEAPON", "", masterData)
    # 武器名
    data["WEAPON"] = ""
    # 皮肤名称
    data["SKIN_NAME"] = ""
    # 皮肤立绘
    data["SKIN_IMAGE"] = ""
    # 皮肤战斗图片
    data["SKIN_SPRITE"] = ""
    # 喜欢
    data["FAVORITE"] = ""
    # 评价等级
    data["HERO_RANK"] = ""
    masterData = {'CATEGORY_NAME': '评价等级', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "FE_RANK", "", masterData)
    # 抽中flag
    data["PICK_FLAG"] = ""
    # 标签
    data["TAGS"] = ""
    # 登录日期
    data["RELEASE_DATE"] = ""


# 没有指定条件时,全取得
if len(FILTER_NAMES) > 0:
    for name in FILTER_NAMES:
        data = CrawlerUtils.initData(DATA_MODEL,{"NAME": name})
        getDetail(data)
        print(CrawlerUtils.formateJSON(data))
else:
    getDateList(result[3])

# 更新master信息
#DBUtil.updateCrawlerMaster(MASTER_DATA)

# 关闭数据库连接
DBUtil.closeConnection()
print("End")
