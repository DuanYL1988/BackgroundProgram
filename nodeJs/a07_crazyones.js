/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/07_crazyones/"
// 保存json文件
const JSON_FILE = "./resources/data/data_crazyones.json"
// 基本域名
const BASE_HOST = "https://wiki.biligame.com/crazyones/"
const IMG_HOST = "https://patchwiki.biligame.com/images/crazyones/"
// 持久化相关
const TBL_NAME = "crazyones"
const PK_ATTR = "name"
var CONNECT = {}
var dbModel = {}
var masterMap = {}
// 下载开关
const DL_FLAG = true//true  false
const OVERRIDE_FLAG = false

// 符合条件的数据
let singleMap = []
// 跳过的数据
let notMap = []
let startIndex = 0 // 0

/** 处理开始 */
if (singleMap.length == 0) {
    // 批量处理
    main()
} else {
    // 单个处理
    for (let i = 0; i < singleMap.length; i++) {
        let currentData = createObject(singleMap[i])
        single(currentData)
    }
}

/**
 * 主处理
 */
async function main() {
    start()
    // 取得一览列表
    let listUrl = BASE_HOST + "卡片图鉴"
    // 发送请求,将响应内容写入文件
    const $ = await util.getTargetElementByAxios(listUrl, "table#CardSelectTr", "templateList.html", true)
    // 开始取得一览
    let dataList = getListInfo($)
    // 开始取得详细情报 dataList.length
    console.log("开始取得详细信息,Total" + dataList.length)
    for (let i = startIndex; i < dataList.length; i++) {
        let currentData = dataList[i]
        console.log("进度 : " + (i + 1) + "/" + dataList.length + ", name : " + currentData[PK_ATTR])
        await getDetailInfo(currentData)
    }
    end()
}

/**
 * 解析一览情报
 * @param {一览请求返回的html内容} $ 
 * @returns 
 */
function getListInfo($) {
    let dataList = []
    $("tbody>tr").each((i, row) => {
        if (i > 0) {
            let tds = $(row).find("td")
            // 名称
            let name = findElementAttr($,tds[1],"a","title",0)
            if (notMap.indexOf(name) < 0) {
                let record = createObject(row)
                let imgSrc = util.getSplitLast(findElementAttr($,tds[0],"img","srcset",0),",", false)
                imgSrc=util.replaceNetImgUrl(imgSrc,"thumb/")
                record.name = name
                record.cardImg = imgSrc
                dataList.push(record)
                createMaster("heroine", "隶属女主角", record.heroine, record.heroine, "", "")
            }
        }
    })
    return dataList
}

/**
 * 解析单个情报
 * @param {单个数据} currentData 
 */
async function getDetailInfo(currentData) {
    let dlImgBox = []
    let localPicNm = currentData.heroine + "/" + currentData.name + util.getSplitLast(currentData.cardImg, ".", true)
    dlImgBox.push(createDLObject(IMG_DIR + localPicNm, currentData.cardImg))
    // 图片下载
    if (DL_FLAG) {
        util.createFolder(IMG_DIR + currentData.heroine)
        await util.downloadImages(dlImgBox, IMG_HOST)
    }
    // 登录DB
    await dbUtil.insetUpdateData(dbModel, currentData, { PK_ATTR: currentData[PK_ATTR] })
    // 写入json
    await util.saveJson(currentData, JSON_FILE)
}

/**
 * 开始处理
 */
async function start() {
    console.log("Start")
    // 初始化json文件
    if (startIndex == 0) {
        util.deleteFile(JSON_FILE)
        util.saveJson("const dataList = [", JSON_FILE)
    }
    // 创建文件夹
    util.createFolder(IMG_DIR)
    // 取得DB连接情报
    CONNECT = await dbUtil.getConnection()
    dbModel = CONNECT.model(TBL_NAME, Schema[TBL_NAME])
    dbMaster = CONNECT.model("code_master", Schema["code_master"])
}

/**
 * 结束处理
 */
async function end() {
    util.saveJson("]", JSON_FILE)
    // 
    for(let key in masterMap) {
        let mstData = masterMap[key]
        console.debug(mstData)
        // 登录DB
        await dbUtil.insetUpdateData(dbMaster, mstData, { categoryId: mstData.categoryId, code: mstData.code })
    }
    // 关闭连接
    CONNECT.disconnect()
    console.log("End")
}
/** ===============私有方法==================== */
/** 取得子元素中属性值
 * @param $ cheerio对象
 * @param parentEle 父元素
 * @param elementName 子元素名 
 * @param index 子元素位置,默认为0
 */
function findElementAttr($,parentEle,elementName,attrName,index) {
    index = typeof index == 'undefined' ? 0 : index
    let targetElemet = $(parentEle).find(elementName)
    if (targetElemet.length > 0 ){
        return targetElemet[index]["attribs"][attrName].trim()
    } else {
        return ''
    }
}

/** ===============构造器==================== */

function createDLObject(localPath, netSrc) {
    return {
        "localNm": localPath
        , "netSrc": netSrc
        , "downloadFlag": DL_FLAG
        , "overRadeFlag": OVERRIDE_FLAG
    }
}

/**
 * 数据模板
 * @returns 
 */
function createObject(trRow) {
    return {
        "name" : ""
        , "cardImg": "String"
        , "rarity": trRow.attribs["data-param3"].substring(0,2)
        , "heroine": trRow.attribs["data-param1"]
        , "type": trRow.attribs["data-param2"]
        , "favorite": "9"
    }
}

/**
 * Master数据模板
 * @returns 
 */
function createMaster(categoryId, categoryName, code, name, localSrc, netSrc) {
    masterMap[categoryId + "_" + code] = {
        "application": TBL_NAME
        , "categoryId": categoryId
        , "categoryName": categoryName
        , "code": code
        , "name": name
        , "imgUrl": localSrc
        , "linkUrl": netSrc
        , "roleGroup": ""
        , "parentId": ""
        , "memo1": ""
        , "memo2": ""
        , "memo3": ""
        , "numberCol1": ""
        , "numberCol2": ""
        , "numberCol3": ""
    }
}
