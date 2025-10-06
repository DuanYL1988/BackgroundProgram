/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')

// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/05_genshin/"

// 保存json文件
const JSON_FILE = "./resources/data/data_genshin.json"
// 基本域名
const BASE_HOST = "https://genshin-impact.fandom.com/ja/wiki/"
const IMG_HOST = "https://static.wikia.nocookie.net/gensin-impact/images/"
// 持久化相关
const TBL_NAME = "genshin"
const PK_ATTR = "name"
var CONNECT = {}
var dbModel = {}
// 下载开关
const imgDlFlag = true//true  false
const OVERRIDE_FLAG = false

// 符合条件的数据
let singleMap = []
// 跳过的数据
let notMap = ["旅人"]
let startIndex = 0 // 0

/** 处理开始 */
if (singleMap.length == 0) {
    main()
} else {
    //start()
    for(let i=0; i<singleMap.length; i++) {
        let currentData = createObject(singleMap[i])
        single(currentData)
    }
    //end()
}

async function single(currentData) {
    let dlImgBox = []
    // 基本信息链接
    let detailLink = BASE_HOST + currentData["name"]
    // 取得数据
    await getDetail(detailLink, currentData, dlImgBox)
    // 图片下载
    if(imgDlFlag) {
        util.createFolder(IMG_DIR + currentData["name"])
        await util.downloadImages(dlImgBox, IMG_HOST)
    }
    // 登录DB
    await dbUtil.insetUpdateData(dbModel, currentData,  { PK_ATTR: currentData[PK_ATTR] })
    // 写入json
    await util.saveJson(currentData, JSON_FILE)
}

async function main() {
    start()
    // 取得一览列表
    let listUrl = BASE_HOST + "キャラクター/一覧"
    // 发送请求,将响应内容写入文件
    const $ = await util.getTargetElementByAxios(listUrl, "table.article-table", "templateList.html", true)
    // 开始取得一览
    let dataList = getListInfo($)

    // 开始取得详细情报 dataList.length
    console.log("开始取得详细信息,Total" + dataList.length)
    /**/
    for (let i = startIndex; i <dataList.length ; i++) {
        let currentData = dataList[i]
        console.log("进度 : " + (i + 1) + "/" + dataList.length + ", name : " + currentData[PK_ATTR])
        if (currentData.sex =="女性") {
            await single(currentData)
        }
    }
    end()
}

async function start(){
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
}

function end(){
    util.saveJson("]", JSON_FILE)
    // 关闭连接
    CONNECT.disconnect()
    console.log("End")
}

function getListInfo($) {
    let dataList = []
    $("tbody>tr").each((i, row) => {
        if (i > 0) {
            let tds = $(row).find("td")
            // 名称
            let name = findElementAttr($,tds[1],"a","title")
            if (notMap.indexOf(name) < 0) {                
                let record = createObject(name)
                // 头像
                let faceSrc = util.replaceNetImgUrl($(tds[0]).find("img")[0].attribs['data-src'], 'images/')
                record.faceImgUrl = faceSrc
                // 稀有度
                let rarity = findElementAttr($,tds[2],"img","alt")
                record.rarity = rarity
                // 元素
                let element = findElementAttr($,tds[3],"a","title") 
                record.element = element
                // 武器
                let weaponType = findElementAttr($,tds[4],"a","title") 
                record.weaponType = weaponType
                // 国家
                let country =  findElementAttr($,tds[5],"a","title") 
                record.country = country
                // 性别
                let sex = findElementAttr($,tds[6],"a","title") 
                sex = sex.indexOf("男性") >= 0 ? "男性" : "女性"
                record.sex = sex
                // releaseDate
                let releaseDate = $(tds[7]).html().trim()
                releaseDate = releaseDate.replace("年", "/").replace("月", "/").replace("日", "")
                record.releaseDate = releaseDate
                dataList.push(record)
            }
        }
    })
    return dataList
}

async function getDetail(detailLink, currentData, dlImgBox) {
    var $ = await util.getTargetElementByAxios(detailLink, "div.pi-image-collection,wds-tabber", "templateDetail.html", true)
    dlImgBox.push(createDLObject(IMG_DIR + currentData.name, currentData.faceImgUrl))
    // 立绘
    let images = $("img")
    currentData.cardImg = util.replaceNetImgUrl(images[0]['attribs']['src'], 'images/')
    dlImgBox.push(createDLObject(IMG_DIR + currentData.name, currentData.cardImg))
    
    $ =  await util.getTargetElementByAxios(detailLink + "/ギャラリー", "div#mw-content-text>div.mw-parser-output", "templateGallery.html", true)
    // 没有 ギャラリー 页面的角色
    if ("error" == $) {
        return
    } else {
        let skinIndex = 0
        $("h3").each((index,title)=>{
            let titleSpan = $(title).find("span.mw-headline")[0]["children"][0].data
            // デフォルト
            if(titleSpan == "デフォルト") {
                let imgDiv = $(title).next()[0]
                if (!util.isEmpty(imgDiv)) {
                    skinIndex = index + 1
                    let img = getImgSrcInDiv($,imgDiv, 3)
                    currentData.fullWish = util.replaceNetImgUrl(img, 'images/')
                    dlImgBox.push(createDLObject(IMG_DIR + currentData.name, currentData.fullWish))
                }
            }
            // 皮肤
            else if (index == skinIndex && titleSpan !== "名刺の飾り紋" && skinIndex > 0) {
                let imgDiv = $($(title).next()).next()
                if (!util.isEmpty(imgDiv)) {
                    let img = getImgSrcInDiv($,imgDiv, 3)
                    currentData.skinImg = util.replaceNetImgUrl(img, 'images/')
                    dlImgBox.push(createDLObject(IMG_DIR + currentData.name,  currentData.skinImg))
                }
            }
        })
        // イラスト
        let imgDiv = getImgDivByTitleSpan($,"イラスト")
        if (!util.isEmpty(imgDiv)) {
            let img = getImgSrcInDiv($,imgDiv, 0)
            currentData.illustration =  util.replaceNetImgUrl(img, 'images/')
            dlImgBox.push(createDLObject(IMG_DIR + currentData.name,  currentData.illustration))
        }

        // 誕生日,祝日
        imgDiv = getImgDivByTitleSpan($,"誕生日")
        if (!util.isEmpty(imgDiv)) {
            $(imgDiv).find("img").each((index, imgEle)=>{
                let imgSrc = util.replaceNetImgUrl(imgEle["attribs"]["data-src"], 'images/')
                currentData.birthday.push(imgSrc)
                dlImgBox.push(createDLObject(IMG_DIR + currentData.name,  imgSrc))
            })
        }

        imgDiv = getImgDivByTitleSpan($,"祝日")
        if (!util.isEmpty(imgDiv)) {
            $(imgDiv).find("img").each((index, imgEle)=>{
                // 00_Artwork
                let imgSrc = util.replaceNetImgUrl(imgEle["attribs"]["data-src"], 'images/')
                currentData.artwork.push(imgSrc)
                dlImgBox.push(createDLObject(IMG_DIR + "00_Artwork",  imgSrc))
            })
        }
    }
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

/** 通过span名取得平行div
 * @param $ cheerio对象
 * @param id 父元素
 */
function getImgDivByTitleSpan($,id) {
    let span = $("span#" + id)[0]
    let parent = $(span).parent()[0]
    let nextDiv = $(parent).next()[0]
    return nextDiv
}

/** 取得div内第index个图片元素
 * @param $ cheerio对象
 * @param parentDiv 父DIV'
 * @param index 图片下标
 */
function getImgSrcInDiv($,parentDiv, index) {
    let imgEle = $(parentDiv).find("img")[index]
    return imgEle["attribs"]["data-src"]
}

/** ===============构造器==================== */

function createDLObject (localPath, netSrc) {
    return {
        "localNm": localPath + util.getSplitLast(netSrc, "/", true)
        , "netSrc": netSrc
        , "downloadFlag": imgDlFlag
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
        , "faceImgUrl" : ""
        , "rarity": ""
        , "weaponType": ""
        , "element": ""
        , "sex": ""
        , "country": ""
        , "releaseDate": ""
        , "cardImg": ""
        , "fullWish": ""
        , "illustration": ""
        , "skinImg" : ""
        , "birthday" : []
        , "artwork" : []
    }
}

/**
 * Master数据模板
 * @returns 
 */
function createMaster(categoryId, categoryName, code, name, localSrc, netSrc) {
    return {
        "application": "genshin"
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
