/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/08_pathToNowhere/"
// 保存json文件
const JSON_FILE = "./resources/data/data_pathToNowhere.json"
// 基本域名
const BASE_HOST = "https://wiki.biligame.com"
const IMG_HOST = "https://patchwiki.biligame.com/images/wqmt/"
// 持久化相关
const TBL_NAME = "pathToNowhere"
const PK_ATTR = "cardImg"
var CONNECT = {}
var dbModel = {}
var masterMap = {}
// 下载开关
const DL_FLAG = false//true  false
const OVERRIDE_FLAG = false

// 符合条件的数据
let singleMap = []
// 跳过的数据
let notMap = ["多芙","L.L.","F.F.","简","蓝鹫","伊琳娜","伊格尼"]
let startIndex = 0 // 0

/** 处理开始 */
main()

/**
 * 主处理
 */
async function main() {
    start()
    // 取得一览列表
    let listUrl = BASE_HOST + "/wqmt/首页"
    // 发送请求,将响应内容写入文件
    const $ = await util.getTargetElementByAxios(listUrl, "div.resp-tabs-container", "templateList.html", true, 0)
    // 开始取得一览 
    let dataList = getListInfo($)
    // 开始取得详细情报
    console.log("开始取得详细信息,Total : " + dataList.length)
    for (let i = startIndex; i < dataList.length; i++) {
        let currentData = dataList[i]
        console.log("进度 : " + (i + 1) + "/" + dataList.length + ", name : " + currentData.name)
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
    $("div.txd>a").each((i, aEle) => {
        // 名称
        let name = aEle.attribs.title
        // 跳过的数据且如果设置单个数据时满足条件
        if (notMap.indexOf(name) < 0 && (singleMap.length ==0 || singleMap.indexOf(name) >= 0)) {
            let record = createObject(name)
            record.link = aEle.attribs.href
            let imgEle = $(aEle).find("img")[0]
            let imgSrc = util.replaceNetImgUrl(imgEle.attribs.alt, "wqmt/")
            record.cardImg = imgSrc
            dataList.push(record)
            // createMaster("heroine", "隶属女主角", record.heroine, record.heroine, "", "")
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
    // cardImg
    let localPicNm = currentData.name + "/cardImg" + currentData.cardImg.substring(currentData.cardImg.indexOf("."))
    dlImgBox.push(createDLObject(IMG_DIR + localPicNm, currentData.cardImg))
    await getDetail(currentData, dlImgBox)
    // 图片下载
    if (DL_FLAG) {
        util.createFolder(IMG_DIR + currentData.name)
        await util.downloadImages(dlImgBox, IMG_HOST)
    }
    // 登录DB
    await dbUtil.insetUpdateData(dbModel, currentData, { cardImg: currentData["cardImg"] })
    // 写入json
    await util.saveJson(currentData, JSON_FILE)
}

async function getDetail(currentData, dlImgBox) {
    const $ = await util.getTargetElementByAxios(BASE_HOST + currentData.link, "div.resp-tabs-container", "templateDetail.html", true, 2)
    $("a").each((index, aEle)=>{
        let localFileNm = aEle.attribs.title.replace("文件:","")
        let imgEle = $(aEle).find("img")[0]
        let imgSrc = ""
        if (imgEle.attribs.alt.indexOf("images/wqmt") > 0) {
            imgSrc = util.replaceNetImgUrl(imgEle.attribs.alt, "wqmt/")
        } else {
            imgSrc = util.replaceNetImgUrl(imgEle.attribs.src, "thumb/")
        }
        let localPicNm = currentData.name + "/" + localFileNm
        currentData.illustration.push(imgSrc)
        dlImgBox.push(createDLObject(IMG_DIR + localPicNm, imgSrc))
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
    for (let key in masterMap) {
        let mstData = masterMap[key]
        console.debug(mstData)
        // 登录DB
        // await dbUtil.insetUpdateData(dbMaster, mstData, { categoryId: mstData.categoryId, code: mstData.code })
    }
    // 关闭连接
    CONNECT.disconnect()
    console.log("End")
}
/** ===============私有方法==================== */


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
function createObject(name) {
    return {
        "name": name
        , "cardImg": ""
        , "rarity": ""
        , "type": ""
        , "favorite": "9"
        , "illustration" : []
        , "link" : ""
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
