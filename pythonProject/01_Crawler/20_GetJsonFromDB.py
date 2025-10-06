# 通用工具类
import ExcelUtils
import CrawlerUtils
import DBUtil

# DDL文件路径
DDL_EXCEL_PATH = "D:\\Project\\VBA\\DDL.xlsx"
OUTPUT_JSON_PATH = "D:\\Project\\htmlProject\\20_CrawlerResult\\"

# 数据名称
TABLE_NAME = "ARKNIGHTS_OPERATOR"

def getAllDataFromDB():
    # excel范围
    range = {"startRow":4, "startCol":1, "endCol":13}
    columns = []
    attrs = []
    inputType = []
    # 取得字段的驼峰名
    for colunm in ExcelUtils.getColumnInfoFromSheet(DDL_EXCEL_PATH, TABLE_NAME, range):
        columns.append(colunm[0])
        attrs.append(colunm[2])
        inputType.append(colunm[8])
    print(inputType)
    dataList = DBUtil.doSearch(TABLE_NAME, columns, {})
    resultList = []
    for rowData in dataList:
        result = {}
        for index,attr in enumerate(attrs):
            if "list" == inputType[index]:
                if rowData[index] is not None:
                    result[attr] = rowData[index].split(",")
                else:
                    result[attr] = []
            else:
                value = rowData[index]
                if value is None:
                    value = "''"
                result[attr] = value
            if rowData[0] == "YD25":
                print(f'{inputType[index]}-{attr}:{rowData[index]} -> {result[attr]}')
        resultList.append(result)
    return resultList

searchResult = getAllDataFromDB()
CrawlerUtils.outputJsonCsv(OUTPUT_JSON_PATH,TABLE_NAME,searchResult)