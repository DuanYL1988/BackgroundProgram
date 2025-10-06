/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
const Master = require('./resources/master.json')

// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/02_fgo/"
// 爬取礼装图片存放路径 
const ART_DIR = "../00_illustration/02_fgo/00_Artwork"
const CE_DIR = "../00_illustration/02_fgo/01_CraftEssences"
const STORY_DIR = "../00_illustration/02_fgo/02_Story"
// 保存json文件
const JSON_FILE = "./resources/data/data_fgo.json"
// 基本域名
const BASE_HOST = "https://fategrandorder.fandom.com"
const url = BASE_HOST + '/wiki/Sub:#name#/Gallery'
const IMG_HOST = "https://static.wikia.nocookie.net/fategrandorder/images/"
// 下载开关
var DL_FLAG = true//true  false
const OVERRIDE_FLAG = false
var dlImgBox = []
//
const MODEL = "fgo_servant"
// 一些匹配关系, 省略if else判断
const IMG_TYPE = Master.imgType
const ATTR_MP = Master.attrsMp

const notMp = {"S154":"-", "S001":"-"}
const NAME = "S002_Artoria Pendragon" // S418_Mysterious Executor C.I.E.L

var masterInfo = {}
/** 处理开始 */
console.log("Start")

if (util.isEmpty(NAME)) {
    main()
} else {
    let servant = createServant(NAME.split("_")[0], NAME.split("_")[1])
    getSingleInfo(servant)
}

/**
 * 取得单个英灵情报
 * @param {英灵信息} servant 
 */
async function getSingleInfo(servant){
    // 取得DB链接
    var conn = await dbUtil.getConnection()
    let dbModel = conn.model(MODEL, Schema[MODEL])
    await getDetail(servant)
    console.log("持久化")
    servant.nameCn = Master.fgoChineseName[servant.no]
    await dbUtil.insetUpdateData(dbModel, servant, {"no" : servant.no})
    end(conn)
}

/**
 * 取得一览url的全部数据
 */
async function main() {
    util.deleteFile(JSON_FILE)
    util.saveJson("const dataList = [", JSON_FILE)
    // 创建文件夹
    util.createFolder(CE_DIR)
    util.createFolder(ART_DIR)
    util.createFolder(STORY_DIR)
    // 取得DB链接
    var conn = await dbUtil.getConnection()
    let dbModel = conn.model(MODEL, Schema[MODEL])
    

    for(let index = 5 ; index > 0 ; index--) {
        // 取得一览列表
        let listUrl = BASE_HOST + "/wiki/Category: " + index + "-Star_Servants"
        const $ = await util.getTargetElementByAxios(listUrl, "table.wikitable")

        let dataList = getListInfo($)
        for (let i=0; i < dataList.length; i++) {
            let servant = dataList[i]
            servant.rarity = index
            console.log("进度 : " + (i + 1) + "/" + dataList.length + ", No : " + servant["no"] + ", name : " + servant["name"])
            let sNo = servant.no.substring(0,4)
            console.debug(sNo)
            if(util.isEmpty(notMp[sNo])) {
                await getDetail(servant)
                servant.nameCn = Master.fgoChineseName[servant.no]
                await dbUtil.insetUpdateData(dbModel, servant, {"no" : servant.no})
                util.saveJson(servant, JSON_FILE)
            } else {
                console.log("warn" ,"当前跳过")
            }
        }

    }
    // 关闭连接
    end(conn)
}

/**
 * 结束处理
 * @param {DB连接} conn 
 */
async function end(conn) {
    // 更新mster
    let masterModel = conn.model("code_master", Schema["code_master"])
    for (let attr in masterInfo) {
        let masterData = masterInfo[attr]
        console.log(masterData)
        await dbUtil.insetUpdateData(masterModel, masterData, { "application": masterData.application, "code": masterData.code, "value": masterData.value })
    }
    // 关闭连接
    conn.disconnect()
    //
    util.saveJson("]", JSON_FILE)
    console.log("End")
}

/**
 * 返回的response解析一览
 * @param {DOM} $ 
 * @returns 
 */
function getListInfo($) {
    let heroList = []
    $("tr").each((index, trEle) => {
        // 跳过第一行标题行
        if (index > 0) {
            $(trEle).find("td > span > a").each((_index, aEle) => {
                // 头像
                let imgEle = $(aEle).find("img")[0]
                // 角色编号
                let keyNo = imgEle.attribs.alt.replace(/A1Icon/, '')
                // 名称
                let name = aEle.attribs.title
                name = name.replace(/"/g,"") // .replace('/', '')
                // 单条数据
                let obj = createServant(keyNo, name)
                heroList.push(obj)
            })
        }
    })
    return heroList 
}

/**
 * 解析图片详细
 * @param {英灵情报} obj 
 */
async function getDetail(obj) {
    dlImgBox = []
    // 发送请求
    console.log("解析图片信息Start")
    const $ = await util.getTargetElementByAxios(obj.detailLink, "div.mw-parser-output")
    getImgInfo($, obj)
    console.log("解析图片信息End")
    // 详细信息
    console.log("解析详细信息Start")
    let detailUrl = "https://fategrandorder.fandom.com/wiki/" + obj.name
    const detailDoc = await util.getTargetElementByAxios(detailUrl, "div.mw-parser-output", "templateDetail.html", true)
    getDetailInfo(detailDoc, obj) 
    console.log("解析详细信息End")
    // 图片下载
    if (DL_FLAG) {
        console.debug(dlImgBox)
        await util.createFolder(IMG_DIR + obj.no + "_" + obj.name.replace(/ /g, '_').replace(":", ""))
        await util.downloadImages(dlImgBox, IMG_HOST)
    }
}

async function getImgInfo($, obj){
    // 保存文件夹
    let dlPath = IMG_DIR + obj.no + "_" + obj.name.replace(/ /g, '_').replace(":", "")
    await util.createFolder(dlPath)
    // 
    $("div.wikia-gallery").each((index, galleryEle) => {
        // 给图片分类
        let titleEle = $(galleryEle).prev()[0]
        titleEle = $(titleEle).find('span.mw-headline')[0]
        let type = IMG_TYPE[$(titleEle).text()]
        // 放入不同的数组
        if (!util.isEmpty(type)) {
            $(galleryEle).find("img").each(async (imgIndex, imgEle) => {
                // 网络图片地址
                let imgSrc = util.replaceNetImgUrl(imgEle.attribs['data-src'])
                // 本地保存图片名称
                let imgName = util.getNameFromPath(imgSrc)
                // 持久化图片(域名一样所以只保存base64转码后部分/0-f/00-ff)
                let saveImgSrc = imgSrc.split('images/')[1]
                // 跳过
                if (imgName.indexOf("MysticEyesSymphony") >= 0) {
                    return
                }
                // 图片名太长的正则匹配
                const imgRex = new RegExp(/_sample\-[0-9a-zA-Z]+/g);
                imgName = imgName.replace(imgRex, '')
                // 一些图片跳过下载 但是不存入DB
                let saveFlag = true
                if ("stage" == type) {
                    if (imgName.indexOf(obj.no + "_") < 0 ){
                        saveFlag = false
                    }
                }
                // ICON
                else if ("icon" == type) {
                    if (imgName.indexOf("IconRaw") < 0 ){
                        // saveFlag = false
                    }
                }
                if (saveFlag) {
                    obj[type].push(saveImgSrc)
                    // 图片保存
                    let path = dlPath
                    // 共用文件夹中保存
                    if ('craftEssences' == type) {
                        path = CE_DIR
                    } else if ('artwork' == type) {
                        path = ART_DIR
                    } else if ('story' == type) {
                        path = STORY_DIR
                    }
                    addImageToBox(path  + '/' + imgName, imgSrc)
                    // 图片下载
                    if (DL_FLAG) {
                        // 图片下载
                        // util.downloadSingleImage(path  + '/' + imgName, imgSrc, OVERRIDE_FLAG)
                    }
                }
            })
        }
    })
}

async function getDetailInfo($, obj) {
    // 职介图标
    let classIconEle = $("div.ServantInfoClass>a>img")[0]
    let iconSrc = "data-src" in classIconEle.attribs ? classIconEle.attribs["data-src"] :  classIconEle.attribs.src
    iconSrc = util.replaceNetImgUrl(iconSrc, 'images/')
    iconInfo = iconSrc.split("-")
    obj.class = iconInfo[1]
    if (iconInfo[2].indexOf("Gold") >= 0) {
        // 登录master
        let master = createMaster("classType", "职阶", iconInfo[1], iconInfo[1], iconSrc)
        masterInfo[iconInfo[1]] = master
    }
    // 名
    $("table.closetable>tbody>tr>td").each((index,tdEle)=>{
        let bEle = $(tdEle).find("b")[0]
        let label = $(bEle).html()
        //
        if ($(bEle).find("a").length > 0) {
            label = $($(bEle).find("a")[0]).html()
        }
        if (!util.isEmpty(ATTR_MP[label])) {
            let attr = ATTR_MP[label]
            let val = ""
            if ("nameJp" == attr || "attr" == attr) {
                val = $(bEle).next()[0]["children"][0].data
                obj[attr] = val
            } else if ("atk" == attr || "hp" == attr) {
                tdEle["children"].forEach(element => {
                    if("text" == element.type) {
                        val = element.data.trim().split("/")[1].replace(",","")
                        obj[attr] = val
                    }
                });
            } else if ("traits" == attr) {
                $(tdEle).find("a").each((_index, aEle) =>{
                    if (_index > 0) {
                        obj[attr].push($(aEle).html())
                    }
                })
            } else if ("voiceActor" == attr || "illustrator" == attr) {
                $(tdEle).find("a").each((_index, aEle) =>{
                    if (_index > 0) {
                        obj[attr] = $(aEle).html()
                    }
                })
            }
        }
    })
}

/**
 * 编辑图片信息.
 * 
 * @param {下载图片的路径} fullPath 
 * @param {图片网络地址} netSrc 
 * @param {下载图片集合} downImgBox 
 */
function addImageToBox(fullPath, netSrc) {
    // 去掉共用部分,服务器地址, 去除扩展名后的版本信息
    if (netSrc.indexOf(IMG_HOST) >= 0) {
        netSrc = util.replaceNetImgUrl(netSrc, 'images/')
        dlImgBox.push({ "localNm": fullPath, "netSrc": netSrc, "downloadFlag": DL_FLAG, "overRadeFlag": OVERRIDE_FLAG })
    }
}

function createServant(no, name) {
    let obj = {
        "no": no,
        "name": name,
        "nameCn": "",
        "nameJp": "",
        "class" : "", // 职介
        "rarity" : "", // 稀有度
        "hp" : "",
        "atk" : "",
        "attr" : "", // 阵营
        "voiceActor" : "", // 声优
        "illustrator" : "", // 画师
        "traits" : [], // 特性
        "breakStage" : "4",
        "stage": [], // 立绘
        "icon": [], // 头像
        "formations": [], // 竖向图标
        "portraits": [], // 半身立绘
        "sprites": [], // 战斗图片
        "craftEssences": [], // 相关礼装
        "artwork": [], // 相关原画
        "story": [], // 相关剧情CG
        "expressionSheets" : [], // 表情集
        "other": [], // 其他
        "detailLink": url.replace(/#name#/, name).replace(/ /g, '_'),
    }
    return obj
}

function createMaster(categoryId, categoryName, code, name, netSrc) {
    return {
        "application": "fgo"
        , "categoryId": categoryId
        , "categoryName": categoryName
        , "code": code
        , "name": name
        , "imgUrl": netSrc
    }
}

/**
 * 添加技能信息
 * @param {技能Code} skillCd 
 * @param {技能名} skillName 
 * @param {技能图标} skillIcon 
 */
function setSkillInfo(skillCd, skillName, skillIcon, type) {
    if(!util.isEmpty(skillCd)) {
        skillList[skillCd] = createSkillInfo(skillCd, skillName, skillIcon, type)
    }
}

function createSkillInfo(skillCd, skillName, skillIcon, skillType) {
    return {
        "game" : "fgo"
        , "skillCd" : skillCd
        , "skillName" : skillName
        , "skillIcon" : skillIcon
        , "skillType" : skillType
    }
}

