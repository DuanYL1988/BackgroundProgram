const util = require('./resources/nodeCommon.js')
const Schema = require('./resources/Schema.json')
const dbUtil = require('./resources/mongoDb.js')
/* 爬取图片存放路径 */
const IMG_DIR = "../00_illustration/03_Azurlane/"
const ACT_DIR = IMG_DIR + "00_Artwork/"
/* 保存数据的json文件 */
const JSON_FILE = "./resources/data/data_azurlane.json"
// 持久化相关
const TBL_NAME = "azurlanes"
const PK_ATTR = "no"
/* 基本域名 */
const BASE_HOST = "https://azurlane.koumakan.jp/wiki/"
var IMG_HOST = "https://azurlane.netojuu.com/images/"
// 下载开关
var DL_FLAG = true//true  false
const OVERRIDE_FLAG = false
// DBmaster数据
var masterInfo = {}
/* 测试用单个网页 539*/
let nameList = [
    "New Jersey", "Enterprise", "Aquila", "Helena", "Cleveland", "North Carolina", "Baltimore", "Washington", "South Dakota", "Yorktown", "Hornet", "Kronshtadt", "Volga", "North Carolina",
    "Hood", "Grenville", "Dido", "Manchester", "Gloucester", "Edinburgh", "Belfast", "Aurora", "London", "Renown", "Exeter", "Black Prince", "Littorio", "Arkhangelsk", "Kiev", "South Dakota",
    "Formidable", "Victorious", "Illustrious", "Ark Royal", "Unicorn", "Queen Elizabeth", "Vanguard", "Duke of York", "Prince of Wales", "King George V", "Rodney", "Nelson", "West Virginia",
    "Takao", "Atago", "Choukai", "Glorious", "Ikazuchi", "Yura", "Mikuma", "Nachi", "Ashigara", "Haguro", "Choukai", "Kii", "Bismarck", "Tirpitz", "Graf Zeppelin", "Yat Sen", "Avrora", "St. Louis",
    "Shinano", "Tosa", "Musashi", "Kaga", "Akagi", "Shoukaku", "Zuikaku", "Taihou", "Shinano", "Leipzig", "Prinz Eugen", "Kawakaze", "Jintsuu", "Noshiro", "Forbin", "Massachusetts", "Yumi",
    "Mikasa", "Dunkerque", "Jean Bart", "Centaur", "Essex", "Memphis", "Friedrich der Große", "Hakuryuu", "Ägir", "Plymouth", "Chitose", "Chiyoda", "Kashino", "Princeton", "Ark Royal", "Honolulu",
    "Minneapolis", "Amagi", "Independence", "Kaga (Battleship)", "Sirius", "Curacoa", "Curlew", "Shangri-La", "Bunker Hill", "Swiftsure", "Le Malin", "Chen Hai", "Hai Tien", "Kongou", "Hiei", "Souryuu",
    "Giulio Cesare", "Zara", "Trento", "Suruga", "Ryuuhou", "Biloxi", "Kirov", "Chapayev", "Sovetsky Soyuz", "Sovetskaya Belorussiya", "Sovetskaya Rossiya", "Bremerton", "Prinz Eugen",
    "Intrepid", "Reno", "Marblehead", "Algérie", "Jeanne d'Arc", "Richelieu", "La Galissonnière", "Vauquelin", "Howe", "Perseus", "Hermione", "Icarus", "Valiant", "Suzutsuki", "Graf Zeppelin",
    "Peter Strasser", "Prinz Heinrich", "Ying Swei", "Penelope", "Tallinn", "Murmansk", "Vittorio Veneto", "Duca degli Abruzzi", "Stephen Potter", "Seydlitz", "Charybdis", "Arizona", "Yat Sen",
    "Ticonderoga", "San Francisco", "Boise", "Katsuragi", "New Orleans", "Foch", "Magdeburg", "Prinz Adalbert", "Ulrich von Hutten", "Columbia", "Wichita", "Pennsylvania", "Nevada",
    "Serri Glaus", "Friedrich Carl", "Poltava", "Chi An", "Liverpool", "Huan Ch'ang", "San Jacinto", "Constellation", "Mary Celeste", "Golden Hind", "Unzen", "Guichen", "Andrea Doria", "Bismarck Zwei",
    "Arizona META", "Trento META", "Scharnhorst META", "Memphis META", "Helena META", "Marco Polo", "August von Parseval", "Anchorage", "Champagne", "Mainz", "Drake", "Azuma", "Seattle", "Saint Louis",
    "Ibuki", "Monarch", "Shimanto", "Kearsarge", "Brest", "Chkalov", "Harbin", "Green Heart", "Murasaki", "Ikaruga", "Lila Decyrus", "Klaudia Valentz", "Reisalin Stout", "Mujina", "Tamaki", "Luna", "Monica", "Nyotengu",
    "Kasumi (Venus Vacation)", "Marie Rose", "Honoka", "Devonshire", "Louisville", "Guam", "Adventure Galley", "Houston II", "Owari", "Clemenceau", "Kersaint", "Suffren", "Marseillaise", "Regensburg", "Otto von Alvensleben",
    "Voroshilov", "Kursk", "Scylla", "Argus", "Implacable", "Ting An", "Hwah Jah", "Theseus", "Kuybyshev", "Northampton II", "Yorktown II", "Hornet II", "Albion", "Roma", "Bolzano", "Leonardo da Vinci", "Joffre", "Revenge",
    "Indomitable", "Elbing", "Emden", "Elbe", "Weser", "Gangut", "Surcouf", "Gneisenau", "Scharnhorst", "Kirishima", "Ardent", "Yorck", "Royal Fortune", "Shirakami Fubuki", "Rikka Takarada", "Asuka"
]

let notMap = ["Painlevé", "São_Martinho", "Brünhilde", "Thüringen", "Lützow", "Maillé_Brézé", "Nürnberg", "Béarn", "La_Galissonnière", "Algérie", "L'Opiniâtre", "Le_Téméraire", "Émile_Bertin"
    , "Blücher", "Köln", "Königsberg", "La_Galissonnière_META"
]

const NO = ""
const MST_NM = "闪乱神乐"
const NM = "Ryuuhou"

if (util.isEmpty(NO)) {
    main()
} else {
    getSingleInfo(NO)
}

async function getSingleInfo(no) {
    console.log("解析单个数据 - Start")
    // 取得DB连接情报
    var conn = await dbUtil.getConnection()
    let shipModel = conn.model(TBL_NAME, Schema[TBL_NAME])
    let masterModel = conn.model("code_master", Schema["code_master"])
    // 取得情报
    let condition = { "no": no }
    let ship = await dbUtil.getDataHasModel(shipModel, condition, true)
    try {
        if (util.isEmpty(ship["name"])) {
            ship = createObject(NM)
            ship.no = no
        }
        await downloadSingle(ship.name, ship)
    } catch (e) {
        console.log(e)
    }
    // 更新DB
    await dbUtil.insetUpdateData(shipModel, ship, condition)
    // 登录master信息
    for (let attr in masterInfo) {
        let masterData = masterInfo[attr]
        masterData["name"] = MST_NM
        await dbUtil.insetUpdateData(masterModel, masterData, { "application": masterData.application, "code": masterData.code, "value": masterData.value })
    }
    // 关闭连接
    conn.disconnect()
    console.log(ship)
    console.log("解析单个数据 - End")
}

async function main() {
    console.log("Start")
    // 初始化json文件
    util.deleteFile(JSON_FILE)
    util.saveJson("const dataList = [", JSON_FILE)
    // 创建文件夹
    util.createFolder(ACT_DIR)

    // 取得DB连接情报
    var conn = await dbUtil.getConnection()
    let dbModel = conn.model(TBL_NAME, Schema[TBL_NAME])

    // 取得一览
    // https://azurlane.koumakan.jp/wiki/List_of_Ships
    const listUrl = BASE_HOST + "List_of_Ships";
    const listDoc = await util.getElementByRequest(listUrl, "table.wikitable", "templateList.html", true)
    return
    let shipList = analysisList(listDoc)

    let masterModel = conn.model("code_master", Schema["code_master"])

    // 取得详细
    for (let i = 0; i < shipList.length; i++) {
        let ship = shipList[i]
        // 图片下载flag, 本地保存flag
        ship.localFlag = nameList.indexOf(ship.name) >= 0 ? true : false
        let name = ship.name.replace(/ /g, '_')
        console.log("进度 : " + (i + 1) + "/" + shipList.length + ", name : " + name + ", localFlag:" + DL_FLAG)
        if (!ship.localFlag) {
            console.log("不是下载对象,跳过")
            continue
        }
        try {
            downloadSingle(name, ship)
        } catch (e) {
            util.writeErrorLog(name, 'azurlane.js', 'getTargetElementByAxios')
        }
        // 登录DB
        await dbUtil.insetUpdateData(dbModel, ship, { "no": ship[PK_ATTR] })
        // 写入json
        if ((i + 1) == shipList.length) {
            await util.saveJson(ship, JSON_FILE, true)
        } else {
            await util.saveJson(ship, JSON_FILE)
        }
        console.log(name + "解析结束")
    }
    // 登录master信息
    for (let attr in masterInfo) {
        let masterData = masterInfo[attr]
        await dbUtil.insetUpdateData(masterModel, masterData, { "application": masterData.application, "code": masterData.code, "value": masterData.value })
    }
    // 关闭连接
    conn.disconnect()
    console.log("End")
}

/**
 * 
 * @param {舰船名} name 
 * @param {舰船对象} ship 
 */
async function downloadSingle(name, ship) {
    // 初始化
    ship.skinList = []
    ship.localSkinList = []
    ship.artImg = []
    ship.localArtImg = []
    // 取得详细信息
    let detailLink = BASE_HOST + name
    console.log(detailLink)
    try {
        const detailDoc = await util.getElementByRequest(detailLink, "div.ship-card", "azuelane.html", true)
        analysisDetail(detailDoc, ship)
        // 截取URL
        let targetUrl = detailLink + '/Gallery'
        // 发送请求 取得内容
        const imgDoc = await util.getElementByRequest(targetUrl, "", "gallery.html", true)
        // 取得皮肤图片
        let imgBox = []
        await analysisSkin(imgDoc, name, imgBox, ship)
        await analysisArtwork(imgDoc, name, imgBox, ship)
        // 建立文件夹
        util.createFolder(IMG_DIR + name)
        if (DL_FLAG) {
            await util.downloadImages(imgBox, IMG_HOST)
        }
    } catch (e) {
        console.log(e)
    }
}

function analysisList($) {
    let list = []
    $("tr").each((index, rowEle) => {
        if (index > 0) {
            let tdList = $(rowEle).find("td")
            if (tdList.length > 0) {
                let ship = createObject()
                ship.no = util.getColHtml(tdList[0])
                ship.name = util.getColHtml(tdList[1])
                ship.rarity = util.getColHtml(tdList[2])
                ship.classification = util.getColHtml(tdList[3])
                ship.faction = util.getColHtml(tdList[4])
                setMaserInfo("rarity", "稀有度", ship.rarity)
                setMaserInfo("classification", "舰种", ship.classification)
                setMaserInfo("faction", "所属", ship.faction)
                list.push(ship)
            }
        }
    })
    return list
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
function analysisDetail($, obj) {
    // 头像
    // 可替换名称
    let faceEle = $("img")[0]
    if (util.isEmpty(faceEle)) {
        obj.faceImgUrl = "{key}"
    } else {
        let faceImgUrl = util.getSplitLast($("img")[0].attribs.src, "images/", false)
        obj.faceImgUrl = faceImgUrl.substring(0, 5) + "{key}"
    }
    // 名
    $("div.card-headline").find("span").each((index, spanEle) => {
        let lang = spanEle.attribs.lang
        if ("zh" == lang) {
            obj.nameCn = $(spanEle).html()
        } else if ("ja" == lang) {
            obj.nameJp = $(spanEle).html()
        }
    })
    // 属性 card-info-tbl
    $("table.card-info-tbl").find("tr").each((index, rowEle) => {
        let key = $($(rowEle).find("th")[0]).html()
        if (null !== key) {
            key = key.toLowerCase()
            let tdEle = $($(rowEle).find("td")[0])
            let value = ""
            if (tdEle.children().length == 0) {
                value = tdEle.html()
            } else {
                let aEle = $(tdEle.find("a")[0])
                if (aEle.find("img").length > 0) {
                    aEle = $(tdEle.find("a")[1])
                }
                value = aEle.html()
            }
            if (key in obj) {
                obj[key] = value.replace(/★/g, '').trim()
            }
        }
    })
    // 所属图标
    console.log()
    let icon = $("div.card-logo").find("img")[0].attribs.src
    icon = icon.replace(/thumb\//, '').split(".png")[0] + ".png"
    setMaserInfo("faction", "", obj["faction"], icon)
}

/**
 * 爬取皮肤图片
 * @param {初始html} html 
*/
async function analysisSkin($, name, imgBox, obj) {
    let fileResult = []
    $('section.mf-section-1 > div.tabber > section > article').each(async (_idx, el) => {
        $(el).find("div.shipskin-image > span >a").each(async (_jdx, fileLink) => {
            fileLink = fileLink.attribs.href
            let imgLink = BASE_HOST + fileLink.replace("/wiki/", "")
            fileResult.push(imgLink)
        })
    })

    for (let i = 0; i < fileResult.length; i++) {
        let imgLink = fileResult[i]
        const fileDoc = await util.getTargetElementByAxios(imgLink, "div#file", "wikiFile.html", true)
        let imgEle = fileDoc("div.fullImageLink").find("a")[0]
        let imgSrc = fileDoc(imgEle).attr('href').split(".png")[0].replace("/thumb", "") + ".png"
        let imgObj = util.splitWebImgSrc(imgSrc)
        let imgNm = imgObj.imgName
        // 取得图片服务器地址
        if (util.isEmpty(IMG_HOST)) {
            IMG_HOST = imgObj.imgHost
        }
        // 国服和谐图片跳过
        if (imgNm.indexOf("CNWithoutBG.png") < 0 && imgNm.indexOf("CN.png") < 0 && imgNm.indexOf("Censored") < 0) {
            let imgPath = IMG_DIR + name + "/" + imgNm
            let dlObj = { "localNm": imgPath, "netSrc": imgObj.splitStr + imgNm, "downloadFlag": true, "overRadeFlag": OVERRIDE_FLAG }
            obj.localSkinList.push(imgNm)
            obj.skinList.push(imgObj.splitStr + imgNm)
            imgBox.push(dlObj)
        }
    }
}

/**
 * 解析请求URL返回的html document
 * @param {html document} html 
 */
async function analysisArtwork($, name, imgBox, obj) {
    let fileResult = []
    $('div.shipgirl-gallery > div.shipgirl-frame > div.shipgirl-art > span > a').each((_idx, el) => {
        let fileLink = $(el).attr("href")
        let imgLink = BASE_HOST + fileLink.replace("/wiki/", "")
        fileResult.push(imgLink)
    })
    for (let i = 0; i < fileResult.length; i++) {
        const fileDoc = await util.getTargetElementByAxios(fileResult[i], "div#file", "wikiFile.html", true)
        let imgEle = fileDoc("div.fullImageLink").find("a")[0]
        const imgSrc = $(imgEle).attr('href')
        let imgObj = util.splitWebImgSrc(imgSrc)
        let imgName = imgObj.imgName
        let netSrc = imgObj.splitStr + imgName
        let dlObj = { "localNm": ACT_DIR + imgName, "netSrc": netSrc, "downloadFlag": true, "overRadeFlag": OVERRIDE_FLAG }
        obj.artImg.push(netSrc)
        obj.localArtImg.push(imgName)
        imgBox.push(dlObj)
    }
    console.log(imgBox)
}

/**
 * 新建master情报
 * @param {category} key 
 * @param {name} codeNm 
 * @param {code} value 
 */
function setMaserInfo(key, codeNm, value, netSrc) {
    let attr = key + "_" + value
    netSrc = util.isEmpty(netSrc) ? "" : netSrc
    if (util.isEmpty(masterInfo[attr])) {
        masterInfo[attr] = createMaster(key, codeNm, value, "", "", netSrc)
    } else {
        masterInfo[attr]["linkUrl"] = netSrc
    }
}

/**
 * 数据模板
 * @returns 
 */
function createObject(name) {
    return {
        "no": ""
        , "name": name
        , "nameCn": ""
        , "nameJp": ""
        , "rarity": ""
        , "classification": ""
        , "faction": ""
        , "illustrator": ""
        , "localFlag": false
        , "faceImgUrl": ""
        , "skinList": []
        , "localSkinList": []
        , "artImg": []
        , "localArtImg": []
    }
}

function createMaster(categoryId, categoryName, code, name, localSrc, netSrc) {
    return {
        "application": "azurlane"
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