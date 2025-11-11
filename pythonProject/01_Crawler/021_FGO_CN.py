# 通用工具类
import CrawlerUtils
import DBUtil
import re
import time

# 数据名称
TABLE_NAME = "FGO_SERVANT"
# 结果输出路径
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\FGO_SERVANT\\"
# 中途开始
BREAK_POINT = 2
# 数据List
DATA_LIST = []
# Master数据
MASTER_DATA = {
  'CLASS_TYPE': {} # 职介
  , 'ATTRS': {} # 属性
  , 'TRAITS': {} # 特性
}
# 爬取方式
RUNWITHREG_FLG = False

'''
从一览取得数据集合
'''
def getDateListByReg():
    # Step.1 读取 HTML 文件
    html_content = ""
    with open("./CrawlerDataFile/fgoWiki.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    # Step.2 使用正则匹配
    pattern = (r'<tr>.*?<td><b>(?P<ID>.*?)</b></td>.*?<td><a href="/w/(?P<NAME_CN>.*?)"><img style.*?</a></td>.*?'
               r'<td>.*?<span lang="ja" style="font-size:x-small;">(?P<NAME_JP>.*?)</span>.*?</span></td>.*?'
               r'<td>.*?</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?'
               r'<td><b>(?P<SUB_ATTRS>.*?)</b></td>.*?<td><b>(?P<EVENT_FLAG>.*?)</b></td>.*?<td><b>(?P<ATTACT>.*?)</b></td>.*?<td><b>(?P<HP>.*?)</b></td>.*?</tr>')
    dataList = CrawlerUtils.getDataListByReg(html_content, pattern)
    for dataCn in dataList:
        if int(dataCn["ID"]) >= BREAK_POINT or "无法获得" == dataCn["EVENT_FLAG"]:
            continue
        key = dataCn["NAME_CN"]
        dataCn["ID"] = "S" + str(int(dataCn["ID"]) + 1000)[1:]
        # 明细
        detailUrl = f'https://fgo.wiki/w/{key}'
        detailDoc = CrawlerUtils.getDomFromUrlByCondition(detailUrl, "div", {"id": "mw-content-text"}, "detailCN.html")
        baseInfoTbl = getSkillDocWithName(detailDoc, "基础数值")
        if baseInfoTbl.name != "table":
            baseInfoTbl= detailDoc.find("table",{"class":"wikitable nomobile graphpicker-container"})
        infoTrs = baseInfoTbl.find_all("tr")
        dataCn["ATTRS"] = infoTrs[6].find_all("td")[4].text.strip()
        dataCn["TRAITS"] = infoTrs[-3].text.replace("、",",").strip()
        # 宝具
        extraNameEle = detailDoc.find("div",attrs={"class":"npname-name"})
        dataCn["SKILL_EXTRA"] = re.sub(r'[A-Za-z\s]', '', extraNameEle.text.strip())
        # 技能
        dataCn["SKILL_1"] = getSkillTxtInTbl(detailDoc, "技能1（初期开放）")
        dataCn["SKILL_2"] = getSkillTxtInTbl(detailDoc, "技能2（灵基再临第1阶段开放）")
        dataCn["SKILL_3"] = getSkillTxtInTbl(detailDoc, "技能3（灵基再临第3阶段开放）")
        
        DBUtil.doUpdate(TABLE_NAME,dataCn,{"ID":dataCn["ID"]})
        time.sleep(3)

def getDateListByDom():
    html_content = ""
    with open("./CrawlerDataFile/fgoWiki.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    htmlDoc = CrawlerUtils.transHtmlToDom(html_content)
    index = 0
    for rowEle in htmlDoc.find_all("tr"):
        index = index + 1
        tdList = rowEle.find_all("td")
        if index == 1 or "无法获得" == tdList[7].text.strip():
            continue
        dataCn = {}
        dataCn["ID"] = "S" + str(int(tdList[0].text.strip()) + 1000)[1:]
        dataCn["NAME_CN"] = tdList[2].find("a").text.strip()
        dataCn["NAME_JP"] = tdList[2].find("span",attrs={"lang":"ja"}).text.strip()
        dataCn["EXTRA_TYPE"] = tdList[3].text.strip()
        dataCn["EXTRA_COLOR"] = CrawlerUtils.matchStr(tdList[3].find("img").get("src"),r'/([^/]+)\.png$')
        dataCn["HP"] = tdList[9].text.strip()
        dataCn["ATTACT"] = tdList[8].text.strip()
        dataCn["EVENT_FLAG"] = "1" if "活动赠送" == tdList[7].text.strip() else ""
        DBUtil.doUpdate(TABLE_NAME,dataCn,{"ID":dataCn["ID"]})

def getSkillTxtInTbl(htmlDoc, text):
    skillTbl = htmlDoc.find_all("b",string=text)
    if len(skillTbl) == 0:
        skillTbl = htmlDoc.find_all("b",string="技能3（灵基再临第4阶段开放）")
    if len(skillTbl) == 0:
        return ""
    parentEle = skillTbl[-1].parent
    tblEle = parentEle.find_next_sibling()
    return tblEle.find("th",attrs={"colspan":"6"}).text.strip()

def getSkillDocWithName(htmlDoc, elementId):
    currentEle = htmlDoc.find(attrs={"id":elementId})
    if currentEle is None:
        currentEle = htmlDoc.find(attrs={"id":elementId+"[1]"})
    parentEle = currentEle.parent
    return parentEle.find_next_sibling()

# 爬取数据
if RUNWITHREG_FLG:
    getDateListByReg()
    # 更新master信息
    #DBUtil.updateCrawlerMaster(MASTER_DATA)
else:    
    getDateListByDom()

# 关闭数据库连接
DBUtil.closeConnection()
print("End")
