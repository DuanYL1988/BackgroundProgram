/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/04_GranblueFantasy/"
// 保存json文件
const JSON_FILE = "./resources/data/data_GranblueFantasy.json"
const FILE_FLAG = true // true, false
// 基本域名
const BASE_HOST = "https://granblue.fandom.com/wiki/" // https://granblue.fandom.com/wiki/SSR_Characters_List
const IMG_HOST = "https://static.wikia.nocookie.net/granblue/images/"
// 持久化相关
const TBL_NAME = "granblue_fantasies"
const PK_ATTR = "name"
var CONNECT = {}
var dbModel = {}
var masterMap = {}
// 下载开关
const DL_FLAG = false//true  false
const OVERRIDE_FLAG = false

// 符合条件的数据
let singleMap = [] //"Zeta (Summer)"
// 跳过的数据
let notMap = []
let startIndex = 0

/** 处理开始 */
main()

async function main() {
    start()
    // 取得一览列表 SSR_Characters_List"
    let raritys = ["SSR", "SR"]
    for(let index = 0; index < raritys.length ; index++) {
        let rarity = raritys[index]
        let listUrl = BASE_HOST + rarity + "_Characters_List"
        // 发送请求 div.mw-parser-output
        const $ = await util.getTargetElementByAxios(listUrl, "div.mw-parser-output", "templateList.html", true)
        // 取得一览内容
        let dataList = getListInfo($)
        // 开始取得详细情报 dataList.length
        console.log("开始取得详细信息,Total" + dataList.length)
        for (let i = startIndex; i < dataList.length; i++) {
            let currentData = dataList[i]
            currentData.rarity = rarity
            console.log("进度 : " + (i + 1) + "/" + dataList.length + ", name : " + currentData[PK_ATTR])
            await getDetailInfo(currentData)
        }
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
    // 开始取得图片位置
    $("tr").each((index, trEle) => {
        if (index > 1) {
            tdList = $(trEle).find("td")
            // 有详细情报的链接
            if ($(tdList[1]).find("a").length > 0) {
                let name = $(tdList[1]).find("a")[0].attribs.title
                let obj = createObj(name)
                // 方便调试,只选一个对象运行,没问题后取反
                if ((singleMap.length == 0 || singleMap.length > 0 && singleMap.indexOf(name) >= 0)
                        && notMap.indexOf(name) < 0) {
                    // table内信息
                    obj.element = getTxtInTd($, tdList[2], 'img', ["element", "元素属性"])
                    obj.type = getTxtInTd($, tdList[3], 'img', ["type", "类型"])
                    obj.race = getTxtInTd($, tdList[4], 'img', ["race", "种族"])
                    obj.weapon = getTxtInTd($, tdList[5], 'img', [])
                    dataList.push(obj)
                }
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
    // 取得数据
    let detailLink = BASE_HOST + currentData.name
    await getDetail(detailLink, currentData, dlImgBox)
    // 图片下载
    if (DL_FLAG) {
        util.createFolder(IMG_DIR + currentData["name"])
        await util.downloadImages(dlImgBox, IMG_HOST)
    }
    // 登录DB
    await dbUtil.insetUpdateData(dbModel, currentData, { PK_ATTR: currentData[PK_ATTR] })
    // 写入json
    if (FILE_FLAG) {
        await util.saveJson(currentData, JSON_FILE)
    }
}

/**
 * 通过详细链接取得单个详细情报
 * 
 * @param {单个数据URL} detailLink 
 * @param {数据} currentData 
 * @param {下载图片盒子} dlImgBox 
 */
async function getDetail(detailLink, currentData, dlImgBox) {
    var $ = await util.getTargetElementByAxios(detailLink, "div.tabber", "templateDetail.html", true)
    // 取得图片div
    $("div.wds-tab__content").find("img").each((index, imgEle) => {
        let imgSrc = imgEle.attribs.src.indexOf('images') > 0 ? imgEle.attribs.src : imgEle.attribs['data-src']
        imgSrc = util.replaceNetImgUrl(imgSrc)
        let saveSrc = util.replaceNetImgUrl(imgSrc, 'images/')
        imgName = saveSrc.split("/")[2]
        // 下载图片
        if (imgSrc.indexOf("_SD") > 0) {
            currentData.sprite.push(saveSrc)
            dlImgBox.push(createDLObject(IMG_DIR + currentData.name , saveSrc))
        } else {
            currentData.artImg.push(saveSrc)
            dlImgBox.push(createDLObject(IMG_DIR + currentData.name , saveSrc))
        }
    })
}

/**
 * 开始处理
 */
async function start() {
    console.log("Start")
    // 初始化json文件
    if (startIndex == 0 && FILE_FLAG) {
        util.deleteFile(JSON_FILE)
        util.saveJson("const dataList = [", JSON_FILE)
    }
    // 创建文件夹
    util.createFolder(IMG_DIR)
    // 取得DB连接情报
    CONNECT = await dbUtil.getConnection()
    dbModel = CONNECT.model(TBL_NAME, Schema[TBL_NAME])
}

/**
 * 结束处理
 */
function end() {
    if (FILE_FLAG) {
        util.saveJson("]", JSON_FILE)
    }
    // 登录master数据
    for (let k in masterMap) {
        // console.debug(k, masterMap[k])
    }
    // 关闭连接
    CONNECT.disconnect()
    console.log("End")
}
/** ===============私有方法==================== */

function getTxtInTd($, td, tagName, mst) {
    let str = ""
    let netSrc = ""
    if ($(td).find(tagName).length > 0) {
        let element = $(td).find(tagName)[0]
        str = element.attribs.alt.split(" ")
        str = str[str.length-1]
        netSrc = typeof(element.attribs["data-src"]) !== "undefined" ? element.attribs["data-src"] : element.attribs["src"]
        netSrc = util.replaceNetImgUrl(netSrc)
    }
    // master
    if(mst.length > 0 && !util.isEmpty(str)) {
        let key = mst[0] + "_" + str 
        let fileNm = key + netSrc.substring(netSrc.lastIndexOf(".")-1)
        let localSrc = "../resources/images/a05/" + fileNm
        let masterData = createMaster(mst[0], mst[1], str, "", localSrc, netSrc)
        masterMap[key] = masterData
    }
    return str
}

/** ===============构造器==================== */

function createDLObject(localPath, netSrc) {
    return {
        "localNm": localPath + util.getSplitLast(netSrc, "/", true)
        , "netSrc": netSrc
        , "downloadFlag": DL_FLAG
        , "overRadeFlag": OVERRIDE_FLAG
    }
}

/**
 * 数据模板
 * @returns 
 */
function createObj(name) {
    return {
        "no": ""
        , "name": name
        , "nameCn": ""
        , "nameJp": ""
        , "rarity" : ""
        , "element": ""
        , "type": ""
        , "race": ""
        , "weapon": ""
        , "artImg": []
        , "sprite": []
    }
}

/**
 * Master数据模板
 * @returns 
 */
function createMaster(categoryId, categoryName, code, name, localSrc, netSrc) {
    return {
        "application": "granblueFantasy"
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