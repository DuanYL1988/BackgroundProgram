/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/04_GranblueFantasy/"
// 保存json文件
const JSON_FILE = "./resources/data/data_GranblueFantasyJP.json"
// 基本域名
const BASE_HOST = "https://xn--bck3aza1a2if6kra4ee0hf.gamewith.jp/article/show/"
const IMG_HOST = "https://img.gamewith.jp/article_tools/granbluefantasy/gacha/"
// 持久化相关
const TBL_NAME = "granblue_fantasies"
const PK_ATTR = "nameJp"
var CONNECT = {}
var dbModel = {}
// 下载开关
const DL_FLAG = false//true  false
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
        
    }
}

/**
 * 主处理
 */
async function main() {
    start()
    // 取得一览列表
    let listUrl = BASE_HOST + "120415"
    // 发送请求,将响应内容写入文件
    const $ = await util.getTargetElementByAxios(listUrl, "table.sorttable,al_chara_table", "templateList.html", true)
    // 开始取得一览 getListInfo($)
    let dataList = getListInfo($)
    // 开始取得详细情报 dataList.length
    console.log("开始取得详细信息,Total:" + dataList.length)
    for (let i = startIndex; i < dataList.length; i++) {
        let currentData = dataList[i]
        // console.log("进度 : " + (i + 1) + "/" + dataList.length + ", name : " + currentData[PK_ATTR])
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
        if (i >= 1) {
            let td = $(row).find("td")[0]
            let href = findElementAttr($, td, "a", "href")
            let icon = util.replaceNetImgUrl(findElementAttr($, td, "img", "data-original"), "gacha/")
            let record = createObject(href, icon, row)
            if ("SSR" == record.rarity) {
                dataList.push(record)
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
    // 基本信息链接
    let detailLink = BASE_HOST + currentData["name"]
    // 取得数据
    // await getDetail(detailLink, currentData, dlImgBox)
    // 图片下载
    if (DL_FLAG) {
        util.createFolder(IMG_DIR + currentData["name"])
        await util.downloadImages(dlImgBox, IMG_HOST)
    }
    // 写入json
    await util.saveJson(currentData, JSON_FILE)
}

/**
 * 通过详细链接取得单个详细情报
 * 
 * @param {单个数据URL} detailLink 
 * @param {数据} currentData 
 * @param {下载图片盒子} dlImgBox 
 */
async function getDetail(detailLink, currentData, dlImgBox) {

}

/**
 * 开始处理
 */
async function start() {
    console.log("Start")
    // 初始化json文件
    if (startIndex == 0) {
        util.deleteFile(JSON_FILE)
        util.saveJson("const dataListJp = [", JSON_FILE)
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
    util.saveJson("]", JSON_FILE)
    // 关闭连接
    CONNECT.disconnect()
    console.log("End")
}
/** ===============私有方法==================== */

function findElementAttr($, td, tagName, attrNm) {
    let str = ""
    if ($(td).find(tagName).length > 0) {
        let element = $(td).find(tagName)[0]
        if ("img" == tagName) {
        }
        str = element.attribs[attrNm]
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
function createObject(href, icon, rowEle) {
    let no = icon.substring(0, icon.indexOf("."))
    return {
        "no": no
        , "transId" : transId(no)
        , "nameJp": rowEle.attribs["data-col1"]
        , "rarity": rowEle.attribs["data-col2"]
        , "element": rowEle.attribs["data-col3"]
        , "race": rowEle.attribs["data-col4"]
        , "type": rowEle.attribs["data-col5"]
        , "weapon": rowEle.attribs["data-col6"]
        , "faceImgUrl" : icon
        , "link" : href.substring(href.lastIndexOf("/")+1)
    }
}

function transId(baseId) {
    const transMp = {
        "3075" : "3077"
        , "3076" : "3075"
        , "3077" : "3076"
        , "3078" : "3079"
        , "3079" : "3080"
        , "3080" : "3078"
        , "3094" : "3095"
        , "3095" : "3094"
        , "3098" : "3099"
        , "3100" : "3101"
        , "3101" : "3100"
        , "3105" : "3106"
        , "3106" : "3107"
        , "3107" : "3105"
        , "3114" : "3115"
        , "3115" : "3116"
        , "3118" : "3120"
        , "3120" : "3123"
        , "3125" : "3127"
        , "3134" : "3136"
        , "3135" : "3137"
        , "3136" : "3135"
        , "3137" : "3138"
        , "3138" : "3141"
        , "3139" : "3140"
        , "3161_03" : "3173"
        , "3170" : "3179"
        , "3171" : "3181"
        , "3172" : "3180"
        , "3173" : "3182"
        , "3174" : "3187"
        , "31XX" : "31XX"
    }
    let id = transMp[baseId]
    if (typeof(id) !=="undefined") {
        return id
    } 
    
    let idint = parseInt(baseId)
    if (idint>=3125 && idint <= 3133) {
        id = idint + 1 
    } else if ((idint>=3140 && idint <= 3144)
        || (idint>=3147 && idint <= 3157)
        || (idint>=3209 && idint <= 3271)
        || (idint>=3284 && idint <= 3352)
        || (idint>=3382 && idint <= 3392)) {
        id = idint + 2
    }  else if ((idint>=3353 && idint <= 3378)
        || (idint>=3393 && idint <= 3412)
        || (idint>=3420 && idint <= 3525)) {
        id = idint + 3
    } else if (idint>=3158 && idint <= 3166) {
        id = idint + 12
    } else if (idint>=3167 && idint <= 3169) {
        id = idint + 15
    }  else if (idint>=3170 && idint <= 3169) {
        id = idint 
    } else {
        id = baseId
    }
    return id
}


