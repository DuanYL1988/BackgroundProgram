/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
const editJson = require('./resources/data/localdata_feh.json')

// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/01_feh/"
const ACT_DIR = IMG_DIR + "00_Art"
const FE0_DIR = "../00_illustration/01_fe0/"
const OTHER_DIR = "../00_illustration/01_feGame/"
// 上传QQ空间路径
const UP_PATH = "C:\\Users\\dylsw\\OneDrive\\图片\\feTemp\\"
// 保存json文件
const JSON_FILE = "./resources/data/data_feh.json"
// 基本域名
const BASE_HOST = "https://feheroes.fandom.com/wiki/"
const FE_WIKI_HOST = "https://fireemblem.fandom.com/wiki/{name}/Gallery"
const IMG_HOST = "https://static.wikia.nocookie.net/feheroes_gamepedia_en/images/"
const FE_IMG_HOST = "https://static.wikia.nocookie.net/fireemblem/images/"
// 持久化相关
const TBL_NAME = "fire_emblem_heros"
const PK_ATTR = "imgName"
// 下载开关
var DL_FLAG = false//true  false
const OVERRIDE_FLAG = false
// 一些匹配关系, 省略if else判断
const HERO_ATTR = {
    "MythicEffect": {code : "blessing", value : "祝福"},
    "LegendaryEffect": {code : "blessing", value : "祝福"},
    "ReleaseDate": {code : "releaseDate", value : ""},
    "Entry": {code : "entry", value : "作品"},
    "InternalID": {code : "nameJp", value : "nameJp"},
    "AllyInternalID": {code : "nameJp", value : "nameJp"},
    "WeaponType": {code : "weaponType", value : "武器类型"},
    "MoveType": {code : "moveType", value : "移动方式"}
}
// 特殊字符
const SPEC_CHAR = {
    "Nerþuz" : "Ner%C3%BEuz"
}

// 单个下载 "Nerþuz: God of the Land"
var NEW_HERO = []
// DBmaster数据
var masterInfo = {}
var skillList = {}

/** 处理开始 */
console.log("Start")

if (NEW_HERO.length > 0) {
    // 特殊字符转换
    for(let i = 0; i < NEW_HERO.length; i++) {
        let name = NEW_HERO[i].split(":")[0]
        let transNm = SPEC_CHAR[name]
        if(!util.isEmpty(transNm)) {
            console.debug("debug2", transNm)
            NEW_HERO[i] = transNm + ":" +NEW_HERO[i].split(":")[1]
        }
    }
    // 爬取数据
    getSingleInfo()
} else {
    main()
    // 复制上传图片
}

/**
 * 单独更新DB
 */
async function updateDbInfo(){
    start()
    // 取得DB连接情报
    var conn = await dbUtil.getConnection()
    let dbModel = conn.model(TBL_NAME, Schema[TBL_NAME])
    // 全取得
    let heroList = await dbUtil.getDataHasModel(dbModel, {}, false)
    // 上个版本的旧数据
    let editMap = util.transListToMap(editJson, PK_ATTR)
    let cnt = 0
    for(let i = 0 ; i < heroList.length; i++) {
        let hero = heroList[i]
        let key = hero[PK_ATTR].replace(/_/g, '')
        if (util.isEmpty(editMap[key])) {
            cnt ++
            hero.pickFlag = 0
            let condition = {"no" : hero.no}
            await dbUtil.insetUpdateData(dbModel, hero, condition)
        }
    }
    console.log("共更新数据: " + cnt)
    end(conn)
}

/**
 * 单独更新一条数据
 * @param {name} name 
 */
async function getSingleInfo() {
    start()
    // 初始化json文件
    util.deleteFile(JSON_FILE)
    await util.saveJson("const dataList = [", JSON_FILE)
    // 取得DB连接情报
    var conn = await dbUtil.getConnection()
    let dbModel = conn.model(TBL_NAME, Schema[TBL_NAME])

    // 取得一览列表
    let listUrl = BASE_HOST + "List_of_Heroes"
    // 发送请求,将响应内容写入文件
    const $ = await util.getTargetElementByAxios(listUrl, "div.mw-parser-output>table", "list.html", true)
    // 开始取得一览
    let dataList = getListInfo($)
    // 开始取得详细情报
    console.log("开始取得详细信息")
    let j = 1
    for (let i = 0; i < dataList.length; i++) {
        let currentData = dataList[i]
        // 是否下载图片
        let newHeroNm = currentData["linkNm"].replace(/_/g, ' ')

        if (NEW_HERO.indexOf(newHeroNm) >= 0) {
            console.log("进度", j , "/" , NEW_HERO.length, "[", newHeroNm, "] exist!!")
            currentData.pickFlag = "1"
            await util.createFolder(IMG_DIR + currentData[PK_ATTR])
            await downloadSingle(currentData, {})
            // 登录DB
            await dbUtil.insetUpdateData(dbModel, currentData, { "imgName": currentData[PK_ATTR] })
            // 写入json
            await util.saveJson(currentData, JSON_FILE)
            if (j == NEW_HERO.length) {
                await util.saveJson("]", JSON_FILE)
            }
            j ++
        }
    }
    if(DL_FLAG) {
        await copyImgToTemp()
    }
    end(conn)
}

async function main() {
    start()
    // 初始化json文件
    util.deleteFile(JSON_FILE)
    util.saveJson("[", JSON_FILE)

    // 取得DB连接情报
    var conn = await dbUtil.getConnection()
    let dbModel = conn.model(TBL_NAME, Schema[TBL_NAME])

    let editMap = util.transListToMap(editJson, PK_ATTR)
    // 手游以外的相册
    let galleryMap = {}
    // 取得一览列表
    let listUrl = BASE_HOST + "List_of_Heroes"
    // 发送请求,将响应内容写入文件
    const $ = await util.getTargetElementByAxios(listUrl, "div.mw-parser-output>table", "list.html", true)
    // 开始取得一览
    let dataList = getListInfo($)
    // 开始取得详细情报
    console.log("开始取得详细信息")
    let totalCnt = dataList.length
    for (let i = 0; i < dataList.length; i++) {
        let currentData = dataList[i]

        // 是否下载图片
        let key = currentData[PK_ATTR].replace(/_/g, '')
        console.log("进度 : " + (i + 1) + "/" + totalCnt + ", name : " + currentData["titleName"] + "," + currentData["linkNm"] + " local : " + currentData.pickFlag)
        // 是否显示
        currentData.pickFlag = util.isEmpty(editMap[key]) ? "0" : "1"
        if (currentData.pickFlag == "1") {
            await util.createFolder(IMG_DIR + currentData[PK_ATTR])
        }
        await downloadSingle(currentData, galleryMap)
        // 登录DB
        await dbUtil.insetUpdateData(dbModel, currentData, { "imgName": currentData[PK_ATTR] })
        // 写入json
        await util.saveJson(currentData, JSON_FILE)
        if ((i + 1) == dataList.length) {
            util.saveJson("]", JSON_FILE)
        }
    }
    end(conn)
}

/**
 * 将下载图片拷贝到上传目录
 */
async function copyImgToTemp(){
    NEW_HERO.forEach(async folderNm => {
        folderNm = folderNm.replace(/:/,'')
        folderNm = folderNm.replace(/ /g,'_')
        if(folderNm.indexOf("Ner%C3%BEuz") >= 0) {
            folderNm = folderNm.replace("Ner%C3%BEuz", "Nerthuz")
        }
        console.log("debug", folderNm)
        let fromPath = IMG_DIR + folderNm + "/01_normal.png"
        let toPath = UP_PATH + folderNm + "_1.png"
        await util.copyFile(fromPath, toPath, false)
        fromPath = IMG_DIR + folderNm + "/02_attact.png"
        toPath = UP_PATH + folderNm + "_2.png"
        await util.copyFile(fromPath, toPath, false)
        fromPath = IMG_DIR + folderNm + "/03_extra.png"
        toPath = UP_PATH + folderNm + "_3.png"
        await util.copyFile(fromPath, toPath, false)
        fromPath = IMG_DIR + folderNm + "/04_break.png"
        toPath = UP_PATH + folderNm + "_4.png"
        await util.copyFile(fromPath, toPath, false)
    })
}

/**
 * 取得单条数据信息
 * @param {单条数据信息} currentData 
 */
async function downloadSingle(currentData, galleryMap) {
    // 初始化
    currentData.stageImg = []
    currentData.cutInImg = []
    currentData.spriteImg = []
    currentData.artImg = []
    let dlImgBox = []
    // 基本信息链接
    let detailLink = BASE_HOST + currentData["linkNm"]
    // 取得数据
    await getDetail(detailLink, currentData, dlImgBox)
    // 相册链接
    let miscLink = BASE_HOST + currentData["linkNm"] + "/Misc"
    await getMiscImg(miscLink, currentData, dlImgBox)
    // merge
    let editMap = util.transListToMap(editJson, PK_ATTR)
    mergeEdited(currentData, editMap)
    // 图片下载
    if (DL_FLAG) {
        // 创建文件夹
        await util.createFolder(IMG_DIR + currentData[PK_ATTR])
        await util.downloadImages(dlImgBox, IMG_HOST)
        // 取得手游以外的情报
        await getGalleryInfo(currentData, galleryMap)
    }
}

/**
 * 通用开始处理
 */
function start() {
    // 创建文件夹
    util.createFolder(IMG_DIR)
    util.createFolder(ACT_DIR)
    util.createFolder(FE0_DIR)
    util.createFolder(OTHER_DIR)
}

async function end(conn) {
    // 更新mster
    let masterModel = conn.model("code_master", Schema["code_master"])
    for (let attr in masterInfo) {
        let masterData = masterInfo[attr]
        await dbUtil.insetUpdateData(masterModel, masterData, { "application": masterData.application, "code": masterData.code, "value": masterData.value })
    }
    // 更新技能
    let skillMode = conn.model("skill_info", Schema["skill_info"])
    for (let attr in skillList) {
        let data = skillList[attr]
        await dbUtil.insetUpdateData(skillMode, data, { "skillCd": data.skillCd})
    }
    // 关闭连接
    conn.disconnect()
    console.log("End")
}

/**
 * 取得一览
 * @param {返回的Html对象} $ 
 * @returns 
 */
function getListInfo($) {
    console.log("开始取得一览信息")
    let dataPrimaryList = []
    $("tr.hero-filter-element").each((index, trEle) => {
        let tdList = $(trEle).find("td > a")
        let heroType = transHeroType(trEle.attribs['data-availability-classes'])
        // 单条数据
        let singleObj = analysisDetail($, trEle, tdList, heroType)
        // 存入集合
        dataPrimaryList.push(singleObj)
    })
    console.log("一览信息取得完毕")
    return dataPrimaryList
}

/**
 * 取得fire emblem相关其他游戏的图片
 * @param {已取得的数据集合} dataPrimaryMap 
 */
async function getGalleryInfo(record, galleryMap) {
    // 人物名
    let baseNm = record["imgName"].split("_")[0]
    if (!(baseNm in galleryMap)) {
        // 初始化列表
        galleryMap[baseNm] = []
        let downloadList = []
        let galleryLink = FE_WIKI_HOST.replace('{name}', baseNm)
        // 发送请求
        const $ = await util.getTargetElementByAxios(galleryLink, "div.mw-parser-output", "templateGallery.html", true)
        if ("error" === $) {
            console.log("该人物没有对应的wiki信息")
            return
        }

        $("h2").each(async (index, titleEle) => {
            // 文件夹
            let fe0Flag = false
            let otherFlag = false
            let titleNm = $($(titleEle).find("span")[0]).html()
            // 有字的卡面全跳过
            if (util.isEmpty(titleNm) || titleNm.indexOf('Trading Cards') >= 0) {
                return
            }
            let divEle = $(titleEle).next()[0]
            $(divEle).find("div.wikia-gallery-item").each((_index, galleryEle) => {
                // 表示的图片名
                let imgNm = $($(galleryEle).find("div.lightbox-caption")[0]).html()
                if (!util.isEmpty(imgNm)) {
                    // 去除tag标签
                    let streg = new RegExp(/<[a-zA-Z]+.*?>/g)
                    let edreg = new RegExp(/<\/[a-zA-Z]*?>/g)
                    imgNm = imgNm.replace(streg, '').replace(edreg, '')
                    // 不要手游的内容
                    if (imgNm.indexOf("Fire Emblem Heroes") < 0 && imgNm.indexOf(" Heroes") < 0
                        && imgNm.indexOf("attacting") < 0 && imgNm.indexOf("animation") < 0 && imgNm.indexOf("sprite") < 0
                        && imgNm.indexOf(" figurine") < 0 && imgNm.indexOf(" model") < 0) {
                        // 图片地址
                        let imgSrc = $(galleryEle).find("img")[0]
                        imgSrc = "data-src" in imgSrc.attribs ? imgSrc.attribs["data-src"] : imgSrc.attribs["src"]
                        imgSrc = util.replaceNetImgUrl(imgSrc, 'images/')

                        if (imgNm.indexOf('Fire Emblem 0 (Cipher)') > 0) {
                            fe0Flag = true
                            imgNm = FE0_DIR + baseNm + "/" + util.getSplitLast(imgSrc, '/', false)
                        } else {
                            otherFlag = true
                            imgNm = titleNm.replace(/ /g, "") + "-" + util.getSplitLast(imgSrc, '/', false).replace('%27', '')
                            imgNm = OTHER_DIR + baseNm + "/" + imgNm
                        }
                        let dlObj = { 'localNm': imgNm, 'netSrc': imgSrc, "downloadFlag": true, "overRadeFlag": OVERRIDE_FLAG }
                        galleryMap[baseNm].push(dlObj)
                        downloadList.push(dlObj)
                    }
                }
            })
            if (fe0Flag && DL_FLAG) {
                util.createFolder(FE0_DIR + baseNm)
            }
            if (otherFlag && DL_FLAG) {
                util.createFolder(OTHER_DIR + baseNm)
            }

        })
        if (DL_FLAG) {
            util.downloadImages(downloadList, FE_IMG_HOST)
        }
    }
}

/**
 * 从一览的列表中取得单个情报信息
 * 
 * @param {一览Html对象} $ 
 * @param {单个Element} singleElement 
 * @param {列集合} tdList 
 * @param {类型} heroType 
 * @returns 
 */
function analysisDetail($, singleElement, tdList, heroType) {
    let obj = createObject()
    let aEle = $(tdList[0])
    let imgEle = $(aEle).find("img")[0]
    // 详细URL
    obj["linkNm"] = tdList[0].attribs.href.replace('/wiki/', '')
    // 角色编号
    let baseName = imgEle.attribs.alt.replace(/ /g, '_').replace(/'/g, '')
    obj[PK_ATTR] = baseName.split('_Face_FC')[0]
    obj["name"] = imgEle.attribs.alt.split(' ')[0]
    obj["titleName"] = obj[PK_ATTR].replace(obj["name"], '').replace(/_/g, '')
    // 头像
    obj["faceImgUrl"] = 'data-src' in imgEle.attribs ? imgEle.attribs['data-src'] : imgEle.attribs.src
    // 从tr取得信息
    obj["heroType"] = heroType
    obj["moveType"] = singleElement.attribs['data-move-type']
    obj["weaponType"] = singleElement.attribs['data-weapon-type'].split(" ")[1]
    obj["color"] = singleElement.attribs['data-weapon-type'].split(" ")[0]
    return obj
}

function edtInfoFromLinkNm(linkNm) {
    let obj = createObject()
    let nameArr = linkNm.split(':')
    obj["name"] = nameArr[0]
    obj["linkNm"] = linkNm
    obj["titleName"] = nameArr[1].replace(/_/g, '')
    obj[PK_ATTR] = linkNm.replace(":", "_")
    if (!util.isEmpty(obj["faceImgUrl"])) {
        obj["faceImgUrl"] = "x/xx/{key}"
    }
    obj.pickFlag = "1"
    return obj
}

/**
 * 取得详细信息
 * @param {详细请求返回的html对象} detailLink 
 * @param {下载图片的路径} dlPath 
 * @param {下载图片集合} downImgMap 
 * @param {数据对象} obj 
 * @returns 
 */
async function getDetail(detailLink, obj, downImgBox) {
    // 发送请求
    let $ = await util.getTargetElementByAxios(detailLink, "div.mw-parser-output", "templateDetail.html", true)
    // 图片信息
    let trEles = $("table.hero-infobox").find("tr")
    let illBox = $(trEles[1]).find("div.fehwiki-tabber > a")
    let breakImg = $(trEles[1]).find("div.fehwiki-tabber > p > a")
    // 下载目录
    let dlPath = IMG_DIR + obj[PK_ATTR]
    // 下载图片集合 
    editImgSrc(obj, "faceImgUrl", downImgBox, dlPath + '/00_face.png', obj.faceImgUrl)
    editImgSrc(obj, "stageImg", downImgBox, dlPath + '/01_normal.png', illBox[0].attribs.href)
    editImgSrc(obj, "stageImg", downImgBox, dlPath + '/02_attact.png', illBox[1].attribs.href)
    editImgSrc(obj, "stageImg", downImgBox, dlPath + '/03_extra.png', illBox[2].attribs.href)
    editImgSrc(obj, "stageImg", downImgBox, dlPath + '/04_break.png', breakImg[0].attribs.href)

    // 其他信息
    for (let row = 3; row < trEles.length; row++) {
        // 属性名
        title = getTitle($, trEles[row])
        let attrNm = HERO_ATTR[title]
        // 属性值
        if (!util.isEmpty(attrNm)) {
            getAttrVal($, trEles[row], attrNm, obj)
        }
    }
    $("h3").each((index, titleEle)=>{
        let htitle = $(titleEle).find("span")[0].children[0].data
        let attsTable = $($(titleEle).next()[0])
        let trs = attsTable.find("tr")
        // 有相关内容一览
        if (trs.length > 0) {
            let lasttrs = trs[trs.length - 1]
            // 基础数值
            if ("Level 40 stats" == htitle) {
                let tdArr = $(lasttrs).find("td")
                obj.hp = $(tdArr[1]).html().split("/")[1]
                obj.atk = $(tdArr[2]).html().split("/")[1]
                obj.spd = $(tdArr[3]).html().split("/")[1]
                obj.def = $(tdArr[4]).html().split("/")[1]
                obj.res = $(tdArr[5]).html().split("/")[1]
            } 
            // 武器
            else if ("Weapons" == htitle) {
                let weaponArr = $(lasttrs).find("td")
                obj.weapon = $(weaponArr[0]).find("a")[0].attribs.title
                obj.weaponPower = $(weaponArr[1]).html()
            }
            // 辅助技能
            else if ("Assists" == htitle) {
                // 武器
                let assists = $(lasttrs).find("td")
                obj.skillCd[3] = $(assists[0]).find("a")[0].attribs.title
            }
            // 奥义
            else if ("Specials" == htitle) {
                let assists = $(lasttrs).find("td")
                let specialTds = $(lasttrs).find("td")
                obj.skillCd[4] = $(specialTds[0]).find("a")[0].attribs.title
            } 
            // 技能
            else if ("Passives" == htitle) {
                getSkillS($, attsTable, obj)
            }
        }
    })

}

/**
 * 取得手游的相关相册图片
 * @param {手游的相册的连接} miscLink 
 * @param {数据对象} recode 
 * @param {下载图片集合} downloadBox 
 * @param {下载图片的路径} dlPath 
 * @returns 
 */
async function getMiscImg(miscLink, recode, downloadBox) {
    // 下载目录
    let dlPath = IMG_DIR + recode[PK_ATTR]
    let $ = await util.getTargetElementByAxios(miscLink, "div.mw-parser-output", "templateGallery.html", true)
    // 中文称号
    let titleTble = $("table.wikitable.default").find("span[lang='zh-Hant-TW']")
    if(titleTble.length > 0) {
        recode.titleName = titleTble[0].children[0]["data"].split("　")[0]
        recode.nameCn = titleTble[0].children[0]["data"].split("　")[1]
    }
    // 图片所在element
    let spriteIndex = 1
    let duoIndex = -1
    $("ul.gallery.mw-gallery-traditional > li").each(async (index, liEle) => {
        // 没有上传的图片文件名
        if ($(liEle).find("div.thumb > div > a").length == 0) {
            let notUpdNm = $($(liEle).find("div.thumb")[0]).html()
            let msg = "#" + recode.linkNm + ">" + notUpdNm
            util.writeInfoLog(msg, "a01.js", "getMiscImg")
            return
        }
        let imgNm = $($(liEle).find("div.gallerytext > p")[0]).text().trim()
        let imgSrc = $(liEle).find("div.thumb > div > a")[0].attribs.href// util.replaceNetImgUrl(, "/images")
        let editSrc = util.replaceNetImgUrl(imgSrc, "/images")
        if (util.isEmpty(imgNm)) {
            imgNm = util.getNameFromPath(editSrc)
            imgNm = imgNm.replace(recode.imgName, '')
        }
        // 这些图片跳过
        if (imgNm.indexOf("_pop") > 0 || editSrc.indexOf("_pop") > 0 || imgNm.indexOf("Japanese Twitter") > 0
            || imgNm.indexOf("_AllTex") >= 0 || imgNm.indexOf("Head_") >= 0 || imgNm.indexOf("_Tex") >= 0
            || imgNm.indexOf("sprite") >= 0 || imgNm.indexOf("Uncropped") >= 0 || imgNm.indexOf("Meet Some of") >= 0
            || imgNm.indexOf("Resplendent") >= 0 || imgNm.indexOf("Spritesheet") >= 0) {
            return
        }
        // 存入不同的地方
        if (imgNm.indexOf("BtlFace_BU.") >= 0) {
            // Resplendent神装
            editImgSrc(recode, "cutInImg", downloadBox, dlPath + '/11_cutIn_att.png', imgSrc)
        } else if (imgNm.indexOf("BtlFace_BU_") >= 0) {
            editImgSrc(recode, "cutInImg", downloadBox, dlPath + '/12_cutIn_dmg.png', imgSrc)

        } else if (imgNm.indexOf("Mini_Unit_") >= 0) {
            if (imgNm.indexOf("Idle_No_Wep") > 0) {
                duoIndex++
                spriteIndex = 0
            }
            imgNm = imgNm.replace("Mini_Unit_", "").replace("Idle_No_Wep", "No_Wep").replace("Idle", "Wep")
            let index = spriteIndex + 100 + (duoIndex * 10)
            let loclNm = dlPath + "/sprite_" + (index + "").substring(1) + imgNm
            spriteIndex++
            editImgSrc(recode, "spriteImg", downloadBox, loclNm, imgSrc, "_Mini_Unit_")

        } else if (imgNm.indexOf("art") > 0) {
            imgNm = imgNm.replace(":", "").replace("'", "").replace(".", "").replace('One-Year', '1st')
            imgNm = imgNm + "_" + util.getSplitLast(imgSrc, '/', false)
            let loclNm = ACT_DIR + '/' + imgNm
            editImgSrc(recode, "artImg", downloadBox, loclNm, imgSrc)
        }
    })
}

/** 私有方法区域 */
function getTitle($, trEle) {
    let title = $($(trEle).find("th>span")[0]).html()
    if (util.isEmpty(title)) {
        title = $($(trEle).find("th>a")[0]).html()
    }
    if (util.isEmpty(title)) {
        title = $($(trEle).find("th")[0]).html()
    }
    return title.replace(/ /g, '').trim()
}

function getAttrVal($, trEle, codeInfo, obj) {
    let tdEle = $(trEle).find("td")[0]
    let tdHtml = $(tdEle).html()
    let val = ""
    let attrNm = codeInfo.code
    if ("nameJp" == attrNm) {
        val = util.getTagElement($, tdHtml, 'code').html().replace("PID_", "")
        //let noReg = new RegExp(/[0-9]+/)
        //obj["no"] = noReg.exec(tdHtml)[0]
        let no = tdHtml.substring(tdHtml.indexOf('(')+1,tdHtml.indexOf(')'))
        obj["no"] = no
    } else if ("blessing" == attrNm) {
        val = tdHtml.split(">")[1].replace(/\n/, '')
    } else if ("entry" == attrNm) {
        val = util.getTagElement($, tdHtml, 'a').html()
    } else if ("releaseDate" == attrNm) {
        val = util.getTagElement($, tdHtml, 'time').html()
    } else if ("moveType" == attrNm) {
        val = $(tdEle).find("a")[0].attribs.title
    } else if ("weaponType" == attrNm) {
        val = $(tdEle).find("a")[0].attribs.title
    }
    obj[attrNm] = val.trim()
    // code的对应图片icon
    let imgSrc = $(tdEle).find("img")
    if(imgSrc.length > 0) {
        imgSrc = "data-src" in imgSrc[0].attribs ? imgSrc[0].attribs["data-src"] : imgSrc[0].attribs["src"]
        imgSrc = util.replaceNetImgUrl(imgSrc, 'images/')
        setMaserInfo(attrNm, codeInfo.value, val.trim(), imgSrc)
    }
}

/**
 * 编辑图片信息.
 * 
 * @param {数据对象} obj 
 * @param {属性} attrName 
 * @param {下载图片集合} downImgBox 
 * @param {下载图片的路径} fullPath 
 * @param {图片网络地址} netSrc 
 * @param {替换文字列} replaceWord 
 */
function editImgSrc(obj, attrName, downImgBox, fullPath, netSrc, replaceWord) {
    // 去掉共用部分,服务器地址, 去除扩展名后的版本信息
    if (netSrc.indexOf(IMG_HOST) >= 0 || "artImg" === attrName) {
        netSrc = util.replaceNetImgUrl(netSrc, 'images/')
        downImgBox.push({ "localNm": fullPath, "netSrc": netSrc, "downloadFlag": true, "overRadeFlag": OVERRIDE_FLAG })
    }
    // console.log("debug", netSrc)
    if (util.isEmpty(replaceWord)) {
        // 普通立绘
        if ("artImg" === attrName) {
            netSrc = netSrc.replace(obj[PK_ATTR], "{key}")
        } else {
            netSrc = netSrc.substring(0, 5) + "{key}"
        }
    } else {
        // Q版图片
        netSrc = netSrc.replace(obj[PK_ATTR] + replaceWord, "{key2}")
    }
    if ("string" == typeof obj[attrName]) {
        obj[attrName] = netSrc
    } else {
        obj[attrName].push(netSrc)
    }
}

/**
 * 解析技能信息
 * @param {文档对象} $ 
 * @param {技能表示Table的Html} skillTbl 
 * @param {更新数据对象} obj 
 */
function getSkillS($, skillTbl, obj) {
    let skillGpCnt = []
    $(skillTbl).find("th").each((line, thEle) => {
        if ('rowspan' in thEle.attribs) {
            skillGpCnt.push(parseInt(thEle.attribs.rowspan))
        }
    })
    // 技能1-3的最终技能行下标
    if (skillGpCnt.length >= 2) {
        if (skillGpCnt.length >= 3) {
            skillGpCnt[2] = skillGpCnt[0] + skillGpCnt[1] + skillGpCnt[2]
        }
        skillGpCnt[1] = skillGpCnt[0] + skillGpCnt[1]
    }
    // 取得技能
    let tblTrArr = $(skillTbl).find("tr")
    skillGpCnt.forEach((rowIndex, index) => {
        // 取得技能对应顺序
        let typeRowIndex = index == 0 ? 1 : skillGpCnt[index - 1] + 1
        let type = $($(tblTrArr[typeRowIndex]).find("th")[0]).html().trim()
        let objSkillIndex = 'A' == type ? 0 : 'B' == type ? 1 : 2
        // 技能Icon
        let skilTr = $(tblTrArr[rowIndex]).find("td")
        let iconImgSrc = util.replaceNetImgUrl($(skilTr[0]).find("a")[0].attribs.href)
        //技能名和技能图标
        let skillIcon = iconImgSrc.replace(IMG_HOST, "")
        obj.skillIcon[objSkillIndex] = skillIcon
        let skillCd = $($(skilTr[1]).find("a")[0]).html()
        obj.skillCd[objSkillIndex] = skillCd
    })

}

function transHeroType(type) {
    if (type.indexOf("duo") >= 0) {
        return "连翼英雄"
    } else if (type.indexOf("legendary") >= 0) {
        return "传承英雄"
    } else if (type.indexOf("harmonized") >= 0) {
        return "双界英雄"
    } else if (type.indexOf("mythic") >= 0) {
        return "神阶英雄"
    } else if (type.indexOf("rearmed") >= 0) {
        return "魔器英雄"
    } else if (type.indexOf("ascended") >= 0) {
        return "开花英雄"
    } else if (type.indexOf("attuned") >= 0) {
        return "响心英雄"
    } else if (type.indexOf("regular_5") >= 0) {
        return "SSR"
    } else if ("specialRate" == type || type.indexOf("special") >= 0) {
        return "SR"
    } else {
        return ""
    }
}

function mergeEdited(from, editMap) {
    let key = from[PK_ATTR].replace(/_/g, '')
    let mergeData = editMap[key]
    let mergeAttr = {
        "hp": "hp"
        , "atk": "attact"
        , "spd": "speed"
        , "def": "def"
        , "res": "mdf"
        , "weapon": "weapon"
        , "race": "race"
        , "masterId": "masterId"
        , "limitPlus": "limitPlus"
        , "dragonFlower": "dragonFlower"
        , "favorite": "favorite"
        , "rank": "rank"
    }
    let mergeKeys = Object.keys(mergeAttr)
    // 本地登录完毕的数据同步
    if (from.pickFlag == "1" && !util.isEmpty(mergeData)) {
        for (let i = 0; i < mergeKeys.length; i++) {
            let toAttr = mergeKeys[i]
            let fromAttr = mergeAttr[toAttr]
            if (!util.isEmpty(mergeData[fromAttr])) {
                from[toAttr] = mergeData[fromAttr]
            }
        }
        from.skillName = [mergeData["skillA"], mergeData["skillB"], mergeData["skillC"], mergeData["skillS"], mergeData["skillE"]]
    }
    // 
    for(let i = 0; i < from.skillCd.length; i++) {
        setSkillInfo(from.skillCd[i], from.skillName[i], from.skillIcon[i], i)
    }
}

/**
 * 数据模板
 * @returns 
 */
function createObject() {
    return {
        "no": "",
        "titleName": "",
        "name": "",
        "nameCn": "",
        "nameJp": "",
        "imgName": "",
        "faceImgUrl": "",
        "stageImg": [],
        "cutInImg": [],
        "spriteImg": [],
        "artImg": [],
        "hp": "",
        "atk": "",
        "spd": "",
        "def": "",
        "res": "",
        "blessing": "",
        "moveType": "",
        "heroType": "",
        "weapon": "",
        "weaponPower": "",
        "weaponType": "",
        "entry": "",
        "color": "",
        "race": "",
        "skillCd": ["", "", "", "", ""],
        "skillName": ["", "", "", "", ""],
        "skillIcon": ["", "", ""],
        "releaseDate": "",
        "masterId": "",
        "limitPlus": "",
        "dragonFlower": "",
        "favorite": "",
        "rank": "",
        "pickFlag": 1,
        "linkNm": ""
    }
}

/**
 * 新建master情报
 * @param {category} key 
 * @param {name} codeNm 
 * @param {code} value 
 */
function setMaserInfo(key, codeNm, value, netSrc) {
    let attr = key + "_" + value
    netSrc = util.isEmpty(netSrc) ? "" : "{FEH_IMG}" + netSrc
    if (util.isEmpty(masterInfo[attr])) {
        masterInfo[attr] = createMaster(key, codeNm, value, "", "", netSrc)
    } else {
        masterInfo[attr]["linkUrl"] = netSrc
    }
}

function createMaster(categoryId, categoryName, code, name, localSrc, netSrc) {
    return {
        "application": "fe"
        , "categoryId": categoryId
        , "categoryName": categoryName
        , "code": code
        , "name": name
        , "imgUrl": localSrc
        , "linkUrl": netSrc
    }
}

/**
 * 添加技能信息
 * @param {技能Code} skillCd 
 * @param {技能名} skillName 
 * @param {技能图标} skillIcon 
 */
function setSkillInfo(skillCd, skillName, skillIcon, type) {
    const typeMap = {0 : "A", 1 : "B", 2 : "C" , 3 : "S", 4 : "E"}
    if(!util.isEmpty(skillCd)) {
        skillList[skillCd] = createSkillInfo(skillCd, skillName, skillIcon, typeMap[type])
    }
}

function createSkillInfo(skillCd, skillName, skillIcon, skillType) {
    return {
        "game" : "feh"
        , "skillCd" : skillCd
        , "skillName" : skillName
        , "skillIcon" : skillIcon
        , "skillType" : skillType
    }
}