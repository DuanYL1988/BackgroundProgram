# 安装库
# pip install mysql-connector-python
import mysql.connector
import json
import CrawlerUtils
from datetime import datetime

# 数据模型
MASTER_MODEL = {
    "ID" : "" # 主键
    , "APPLICATION" : "" # 应用
    , "CATEGORY_ID" : "" # 种类ID
    , "CATEGORY_NAME" : "" # 种类名
    , "CODE" : "" # code
    , "NAME" : "" # 名
    , "LINK_URL" : "" # 链接
    , "IMG_URL" : "" # 图片地址
    , "ROLE_GROUP" : "" # 用户权限组
    , "PARENT_ID" : "" # 关联父种类
    , "MEMO1" : "" # 扩展字段1
    , "MEMO2" : "" # 扩展字段2
    , "MEMO3" : "" # 扩展字段3
    , "NUMBER_COL1" : "" # 扩展数字字段1
    , "NUMBER_COL2" : "" # 扩展数字字段2
    , "NUMBER_COL3" : "" # 扩展数字字段3
}

HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = 'duanyl'

connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)

'''
============= 功能性方法 =============
'''
def doSearch(table, columns, condition):
    cols = ""
    columns = columns if isinstance(columns, list) else columns.split(",")
    for col in columns:
        cols += col + ","
    if len(columns) == 0:
        cols = "*"
    else:
        cols = cols[0:-1]
    query = f"SELECT {cols} FROM " + table + concatConditionQuery(condition)
    return doSearchQuery(query)

def SearchOne(table, columns, condition):
    resultArrs = doSearch(table, columns, condition)
    print(f"预计结果:1件,实际结果:{len(resultArrs)}件")
    result = resultArrs[0] if len(resultArrs) == 1 else None
    return result

def getCount(table, condition):
    query = "SELECT COUNT(*) AS count FROM " + table + concatConditionQuery(condition)
    count = doSearchQuery(query)[0][0]
    print(f"<== SUCCESS count:{count}")
    return count

def doSearchQuery(selectQuery):
    cursor = connection.cursor()
    print("==> 开始执行SQL :" + selectQuery)
    cursor.execute(selectQuery)
    result = cursor.fetchall()
    cursor.close()
    return result

def concatConditionQuery(condition):
    query = " where 1 = 1"
    if condition is not None:
        for key in condition:
            value = condition[key]
            if "NULL" == value.upper():
                query = query + " and " + key + " IS NULL"
            elif "NOTNULL" == value.replace(" ","").upper():
                query = query + " and " + key + " IS NOT NULL"
            else:
                query = query + " and " + key + " = '" + value.replace("'","''") + "'"
    return query

def doInsertOrUpdate(table, data, pkInfo):
    existFlag = getCount(table, pkInfo)
    if existFlag == 1:
        doUpdate(table, data, pkInfo)
    elif existFlag == 0:
        doInsert(table, data)

def doInsert(table, data):
    cursor = connection.cursor()
    query = "INSERT INTO " + table + "("
    columnPart = ""
    paramsPart = ""
    valuesPart = []
    for column in data:
        value = data[column]
        if isinstance(value, list):
            value = json.dumps(value, separators=(',', ':'))
        if "" != value:
            columnPart += column + ", "
            valuesPart.append(value)
            paramsPart = paramsPart + "%s, "
    query += columnPart[0:-2] + ") VALUES (" + paramsPart[0:-2] + ")"
    data = (valuesPart)
    print("==> 开始执行Insert Query:")
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    print("<== 成功")

def doUpdate(table, data, pkInfo):
    cursor = connection.cursor()
    query = "UPDATE " + table + " SET "
    valuesPart = []
    for column in data:
        value = data[column]
        if isinstance(value, list):
            value = json.dumps(value, separators=(',', ':'))
        if "" != value:
            query += column + " = %s, "
            valuesPart.append(value)
    query = query[0:-2] + concatConditionQuery(pkInfo)
    data = (valuesPart)
    print(f"==> 开始执行Update Query:")
    cursor.execute(query, data)
    print(f"<== 更新成功:{cursor.rowcount}件")
    cursor.close()
    connection.commit()

def closeConnection():
    connection.close()

'''
============= 业务性方法 =============
'''

'''
爬虫执行完后更新master_code表
'''
def updateCrawlerMaster(masterDataDir):
    now = datetime.now()
    for key in masterDataDir:
        for subKey in masterDataDir[key]:
            keyinfo = subKey.split("-")
            if len(keyinfo) > 2:
                condition = {"APPLICATION": subKey.split("-")[0],"CATEGORY_ID":subKey.split("-")[1],"CODE":subKey.split("-")[2]}
                masterData = CrawlerUtils.initData(masterDataDir[key][subKey], condition)
                masterData["MEMO3"] = now.strftime("%Y-%m-%d %H:%M:%S")
                doInsertOrUpdate("CODE_MASTER",masterData,condition)

'''
爬虫执行过程中编辑数据
'''
def editMasterData(FULL_MASTERDATA, key, subkey, editData):
    masterData = {key + "-" +subkey : CrawlerUtils.initData(MASTER_MODEL, editData)}
    for attr in editData:
        masterData[attr] = editData[attr]
    FULL_MASTERDATA[key].update(masterData)

'''
爬虫执行完后从DB读取数据下载图片
'''
def downloadFehImgFromDB(tableName, condition):
    result = SearchOne(tableName, "IMG_NAME, FACE_IMG, STAGE_IMG, CUT_IN_IMG, SPRITE_IMG, ART_IMG", condition)
    if result is None:
        return
    configration = SearchOne("configration", "img_url,wait_time,LOCAL_DIRECTORY", {"table_name": tableName})
    # 头像
    imgHost = [configration[0],result[0]]
    dataModel = {
        "faceImg": {"src": f"{imgHost[0]}{result[1]}{imgHost[1]}_Face_FC.webp", "name" : "00_face"}
    }
    stageImgsDirt = ["_Face.webp","_BtlFace.webp","_BtlFace_C.webp","_BtlFace_D.webp"]
    fileNames = ["01_normal","02_attact","03_extra","04_break"]
    editListImg(dataModel, "stage", imgHost, result[2], stageImgsDirt, fileNames)
    cutInImgDirt = ["_BtlFace_BU.webp","_BtlFace_BU_D.webp"]
    fileNames = ["11_cutIn_att","12_cutIn_dmg"]
    editListImg(dataModel, "cutIn", imgHost, result[3], cutInImgDirt, fileNames)
    spriteImgDirt = []
    spriteSrc = []
    print(result)
    # 还没有cutin的时候
    for src in json.loads(result[4]):
        netSrc = f"{src[:5]}{result[0]}_Mini_Unit_{src[5:]}"
        spriteSrc.append(netSrc)
        spriteImgDirt.append(f"Mini_Unit_{src[5:]}")
    # TODO 图片url转换后规则未解析
    #editListImg(dataModel, "sprite", imgHost, result[4],spriteSrc, spriteImgDirt)

    print(CrawlerUtils.formateJSON(dataModel))
    targetPath = configration[2] + result[0] + "\\"
    CrawlerUtils.downloadImage(targetPath, dataModel["faceImg"]["name"], dataModel["faceImg"]["src"], False)
    for imgData in dataModel["stage"]:
        CrawlerUtils.downloadImage(targetPath, imgData["name"], imgData["src"], False)
    for imgData in dataModel["cutIn"]:
        CrawlerUtils.downloadImage(targetPath, imgData["name"], imgData["src"], False)

def editListImg(dataModel, attrNm, imgHost, imgNameStr, srcMpNames, fileNames):
    if "[" in imgNameStr and "]" in imgNameStr:
       imgSrcList = json.loads(imgNameStr)
       if len(imgSrcList) > 0:
           dataModel[attrNm] = [] # 初始化
           for index,stageSrc in enumerate(imgSrcList):
               mpName = srcMpNames[index] if len(srcMpNames) > index else ""
               dataModel[attrNm].append({
                   "src": f"{imgHost[0]}{stageSrc}{imgHost[1]}{mpName}"
                   , "name": f"{fileNames[index]}"
               })

#downloadFehImgFromDB("FIREEMBLEM_HERO", {"NAME":"Tiki"})
print("aaa")