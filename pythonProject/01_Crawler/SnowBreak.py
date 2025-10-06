# 通用工具类
import CrawlerUtils
import DBUtil
import time

# 数据名称
TABLE_NAME = "SNOW_BREAK"
# DB取得配置信息
result = DBUtil.SearchOne("configration", "BASE_URL,IMG_URL,WAIT_TIME,LIST_URL,LOCAL_DIRECTORY", {"table_name": TABLE_NAME})
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
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\SNOW_BREAK\\"

# 单独爬取
FILTER_NAMES = []
# 执行断点
BREAK_POINT = 0
# 覆盖flag
OVERWRITE_FLAG = False
# 数据模型
DATA_MODEL = {
    "ID" : "" # 主键ID
    , "TITLE_NAME" : "" # 称号
    , "NAME" : "" # 名
    , "IMG_NAME" : "" # 立绘图片文件夹名
    , "FACE_IMG" : "" # 头像
    , "RARITY" : "" # 稀有度
    , "HP" : "" # 生命
    , "ATK" : "" # 攻击
    , "DEF" : "" # 防御
    , "ELEMENT_TYPE" : "" # 元素属性
    , "WEAPON_TYPE" : "" # 武器类型
    , "WEAPON" : "" # 武器名
    , "SKIN_NAME" : [] # 皮肤名称
    , "SKIN_IMAGE" : [] # 皮肤立绘
    , "LOGISTIC_TEAM" : [] # 后勤小队
    , "LOGISTIC_FACE" : [] # 后勤头像
    , "LOGISTIC_IMG" : [] # 后勤立绘
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
  'SNOW_ELEMENT': {} # 元素属性
  , 'SNOW_WEAPON': {} # 武器类型
}

'''
从一览取得数据集合
'''
def getDateList(listUrl):
    # Step.1 发送请求取得DOM对象
    listDoc = CrawlerUtils.getDomFromUrlByCondition(listUrl, "table", {"id": "CardSelectTr"}, "list.html")

    # Step.2 使用正则匹配
    pattern = (r'<tr class="divsort" data-param1="(?P<VOCATION>.*?)" data-param2="(?P<RARITY>.*?),.*?" data-param3=".*?" data-param4="(?P<INFLUENCE>.*?)" data-param5="(?P<TAGS>.*?)".*?'
               r'<td>.*?</td>\n<td><div class="center">.*?<br/>.*?- (?P<SUB_VOCATION>.*?)\n</td>.*?</tr>')
    dataList = CrawlerUtils.getDataListByReg(str(listDoc), pattern)

    for index, listData in enumerate(dataList):
        # 初始化数据
        data = CrawlerUtils.initData(DATA_MODEL, listData)
        # 筛选条件
        filterKey = data["NAME_CN"]
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
    DBUtil.editMasterData(MASTER_DATA, "SNOW_ELEMENT", "", masterData)
    # 武器类型
    data["WEAPON_TYPE"] = ""
    masterData = {'CATEGORY_NAME': '武器类型', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "SNOW_WEAPON", "", masterData)
    # 武器名
    data["WEAPON"] = ""
    # 皮肤名称
    data["SKIN_NAME"] = ""
    # 皮肤立绘
    data["SKIN_IMAGE"] = ""
    # 后勤小队
    data["LOGISTIC_TEAM"] = ""
    # 后勤头像
    data["LOGISTIC_FACE"] = ""
    # 后勤立绘
    data["LOGISTIC_IMG"] = ""
    # 喜欢
    data["FAVORITE"] = ""
    # 评价等级
    data["HERO_RANK"] = ""
    # 抽中flag
    data["PICK_FLAG"] = ""
    # 标签
    data["TAGS"] = ""
    # 登录日期
    data["RELEASE_DATE"] = ""


# 爬取数据
getDateList(LIST_URL)
CrawlerUtils.outputJsonCsv(OUTPUT_JSON_PATH,TABLE_NAME,DATA_LIST)

# 更新master信息
#DBUtil.updateCrawlerMaster(MASTER_DATA)

# 关闭数据库连接
DBUtil.closeConnection()
print("End")
