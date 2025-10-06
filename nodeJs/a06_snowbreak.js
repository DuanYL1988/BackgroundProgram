/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/06_snowbreak/"
// 保存json文件
const JSON_FILE = "./resources/data/data_snowbreak.json"
const WECHAT_DATA_FILE = "./resources/data/data.js"
// 基本域名
const BASE_HOST = "https://wiki.biligame.com/sonw/"
const IMG_HOST = "https://patchwiki.biligame.com/images/sonw/"
// 持久化相关
const TBL_NAME = "snowbreak"
const PK_ATTR = "name"
var CONNECT = {}
var dbModel = {}
var masterMap = {}
// 开关:true,false
const DB_FLAG = true 
const DL_FLAG = false
const OVERRIDE_FLAG = false

// 符合条件的数据
let singleMap = [] // "里芙·狂猎"
// 跳过的数据
let notMap = []
let startIndex = 6 // 0

main()

/**
 * 主处理
 */
async function main() {
    start()
    // 取得一览列表
    let listUrl = BASE_HOST + "%E8%A7%92%E8%89%B2"
    // 发送请求,将响应内容写入文件
    const $ = await util.getTargetElementByAxios(listUrl, "div.resp-tabs-container", "templateList.html", true)
    // 开始取得一览
    let dataList = getListInfo($)
    // 开始取得详细情报 dataList.length
    console.log("开始取得详细信息,Total:" + dataList.length)
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
    let div = $("div.resp-tab-case")[0]
    $(div).find("img").each((index, imgEle)=>{
        let imgName =  util.getSplitLast(imgEle.attribs.alt, "-", false)
        let name = imgName.substring(0, imgName.indexOf("."))
        if (notMap.indexOf(name) < 0 && (singleMap.length ==0 || singleMap.indexOf(name) >= 0)) {
            let record = createObject(name.replace('·','_'))
            record.cardImg = util.replaceNetImgUrl(imgEle.attribs.src, "sonw/")
            record.link = name
            dataList.push(record)
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
    // 取得数据
    await getDetail(BASE_HOST + currentData.link, currentData, dlImgBox)
    // 图片下载
    if (DL_FLAG) {
        util.createFolder(IMG_DIR + currentData.name)
        await util.downloadImages(dlImgBox, IMG_HOST)
    }
    // 登录DB
    if(DB_FLAG) {
        await dbUtil.insetUpdateData(dbModel, currentData, { "name": currentData[PK_ATTR] })
    }
    // 写入json
    await util.saveJson(currentData, JSON_FILE)
    await util.saveJson(currentData, WECHAT_DATA_FILE)
}

/**
 * 通过详细链接取得单个详细情报
 * 
 * @param {单个数据URL} detailLink 
 * @param {数据} currentData 
 * @param {下载图片盒子} dlImgBox 
 */
async function getDetail(detailLink, currentData, dlImgBox) {
    dlImgBox.push(createDLObject(currentData.name + "/face.png", currentData.cardImg))
    var $ = await util.getTargetElementByAxios(detailLink, "div.resp-tabs-container", "templateDetail.html", true)
    /**/
    $("img").each((index, imgEle) => {
        let imgName = imgEle.attribs.alt.replace(currentData.link, "")
        let type = imgName.substring(0, imgName.indexOf("."));
        if(type.indexOf("立绘") >= 0) {
            currentData.illustration.push(imgEle.attribs.src)
            dlImgBox.push(createDLObject(currentData.name + "/" + imgName, imgEle.attribs.src.replace(IMG_HOST, "")))
        } 
    })
}

/**
 * 开始处理
 */
async function start() {
    console.log("Start")
    // 初始化json文件
    if (startIndex == 0) {
        util.deleteFile(JSON_FILE)
        util.deleteFile(WECHAT_DATA_FILE)
        util.saveJson("const dataList = [", JSON_FILE)
        util.saveJson("export default {\n  'dataList' : [", WECHAT_DATA_FILE)
    }
    // 创建文件夹
    util.createFolder(IMG_DIR)
    // 取得DB连接情报
    if(DB_FLAG) {
        CONNECT = await dbUtil.getConnection()
        dbModel = CONNECT.model(TBL_NAME, Schema[TBL_NAME])
        dbMaster = CONNECT.model("code_master", Schema["code_master"])
    }
}

/**
 * 结束处理
 */
async function end() {
    util.saveJson("]", JSON_FILE)
    util.saveJson("  ]\n}", WECHAT_DATA_FILE)
    // 
    for(let key in masterMap) {
        let mstData = masterMap[key]
        // 登录DB
        if(DB_FLAG) {
            await dbUtil.insetUpdateData(dbMaster, mstData, { categoryId: mstData.categoryId, code: mstData.code })
        }
    }
    // 关闭连接
    if(DB_FLAG) {
        CONNECT.disconnect()
    }
    console.log("End")
}
/** ===============私有方法==================== */


/** ===============构造器==================== */

function createDLObject(localPath, netSrc) {
    return {
        "localNm": IMG_DIR + localPath
        , "netSrc": netSrc
        , "downloadFlag": DL_FLAG
        , "overRadeFlag": OVERRIDE_FLAG
    }
}

/**
 * 数据模板
 * @returns 
 */
function createObject(name) {
    return {
        "name": name
        , "cardImg" : ""
        , "illustration" : []
        , "link" : ""
    }
}

/**
 * Master数据模板
 * @returns 
 */
function createMaster(categoryId, categoryName, code, name, localSrc, netSrc) {
    return {
        "application": "???"
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
