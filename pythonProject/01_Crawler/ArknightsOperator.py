# 通用工具类
import CrawlerUtils
import DBUtil
import time

# 数据名称
TABLE_NAME = "ARKNIGHTS_OPERATOR"
# 基本URL
result = DBUtil.SearchOne("configration", "base_url,img_url,wait_time", {"table_name": TABLE_NAME})
BASE_URL = result[0]
BASE_IMG_URL = result[1]
SLEEP_TIME = result[2]
# 结果输出路径
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\ARKNIGHTS_OPERATOR\\"

# 单独爬取
FILTER_NAMES = [""]
# 执行断点
BREAK_POINT = ""
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
    , "SKIN_NAME" : [] # 皮肤名称
    , "SKIN_ICON" : [] # 皮肤头像
    , "SKIN_SPRITE" : [] # 皮肤战斗图片
    , "SKIN_IMAGE" : [] # 皮肤立绘
    , "DEFALT_SKIN" : "" # 默认皮肤
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
    , "SKILLS" : [] # 技能
    , "SKILLS_ICON" : [] # 技能图标
    , "BUILD_SKILLS" : [] # 基建技能
    , "CAPACITY" : [] # 潜能
    , "RELEASE_DATE" : "" # 实装日期
}

# 数据List
DATA_LIST = []
# Master数据
MASTER_DATA = {
  'ARK-CLASS': {} # 职业
  , 'ARK-CLASS_BRANCH': {} # 副职业
  , 'ARK-INF': {} # 势力
  , 'ARK-INF': {} # 出生地
  , 'ARK-RACE': {} # 种族
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
    # 主键
    data["ID"] = ""
    # 英文名
    data["NAME"] = ""
    # 中文名
    data["NAME_CN"] = ""
    # 日文名
    data["NAME_JP"] = ""
    # 头像
    data["FACE_IMG"] = ""
    # 精1立绘
    data["STAGE_ONE_IMG"] = ""
    # 精2立绘
    data["STAGE_TWO_IMG"] = ""
    # 地图人物图片
    data["SPRITE_IMG"] = ""
    # 皮肤名称
    data["SKIN_NAME"] = ""
    # 皮肤头像
    data["SKIN_ICON"] = ""
    # 皮肤战斗图片
    data["SKIN_SPRITE"] = ""
    # 皮肤立绘
    data["SKIN_IMAGE"] = ""
    # 默认皮肤
    data["DEFALT_SKIN"] = ""
    # 稀有度
    data["RARITY"] = ""
    # 职业
    data["VOCATION"] = ""
    masterData = {'CATEGORY_NAME': '职业', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "ARK-CLASS", "", masterData)
    # 副职业
    data["SUB_VOCATION"] = ""
    masterData = {'CATEGORY_NAME': '副职业', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "ARK-CLASS_BRANCH", "", masterData)
    # 词缀
    data["TAGS"] = ""
    # 势力
    data["INFLUENCE"] = ""
    masterData = {'CATEGORY_NAME': '势力', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "ARK-INF", "", masterData)
    # 出生地
    data["BIRTH_PLACE"] = ""
    masterData = {'CATEGORY_NAME': '出生地', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "ARK-INF", "", masterData)
    # 种族
    data["RACE"] = ""
    masterData = {'CATEGORY_NAME': '种族', 'NAME': '', 'IMG_URL': ''}
    DBUtil.editMasterData(MASTER_DATA, "ARK-RACE", "", masterData)
    # 生命
    data["HP"] = ""
    # 攻击
    data["ATK"] = ""
    # 防御
    data["DEF"] = ""
    # 法抗
    data["RES"] = ""
    # 部署费用
    data["COST"] = ""
    # 技能
    data["SKILLS"] = ""
    # 技能图标
    data["SKILLS_ICON"] = ""
    # 基建技能
    data["BUILD_SKILLS"] = ""
    # 潜能
    data["CAPACITY"] = ""
    # 实装日期
    data["RELEASE_DATE"] = ""


# 没有指定条件时,全取得
if len(FILTER_NAMES) > 0:
    for name in FILTER_NAMES:
        data = CrawlerUtils.initData(DATA_MODEL,{"NAME": name})
        getDetail(data)
        print(CrawlerUtils.formateJSON(data))
else:
    getDateList(result[3])
    CrawlerUtils.outputJsonCsv(OUTPUT_JSON_PATH,TABLE_NAME,DATA_LIST)

# 更新master信息
#DBUtil.updateCrawlerMaster(MASTER_DATA)

# 关闭数据库连接
DBUtil.closeConnection()
print("End")
