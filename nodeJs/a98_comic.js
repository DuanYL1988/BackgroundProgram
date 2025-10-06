/** 通用导入部分 */
const util = require('./resources/nodeCommon')

// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/98_comic/"

// 基本域名
const BASE_HOST = "https://doujin-night.com/%e7%be%8e%e5%b0%91%e5%a5%b3%e6%88%a6%e5%a3%ab%e3%82%bb%e3%83%bc%e3%83%a9%e3%83%bc%e3%83%a0%e3%83%bc%e3%83%b3/%e3%80%90%e3%82%a8%e3%83%ad%e5%90%8c%e4%ba%ba%e8%aa%8c%e3%80%91%e3%81%a4%e3%81%8b%e3%81%be%e3%81%a3%e3%81%9f%e3%82%bb%e3%83%bc%e3%83%a9%e3%83%bc%e6%88%a6%e5%a3%ab%e3%81%9f%e3%81%a1%e3%81%8c%e5%aa%9a/"
// 下载开关
const imgDlFlag = true//true  false
const OVERRIDE_FLAG = false

/** 处理开始 */
main()

async function main() {
    console.log("Start")
    // 创建文件夹
    util.createFolder(IMG_DIR)
    // 发送请求,将响应内容写入文件
    let selector = BASE_HOST.indexOf("eromanga") > 0 ? "div.article" : "section#article"
    const $ = await util.getTargetElementByAxios(BASE_HOST, selector, "gallery.html", true)
    dlImgList = getListInfo($,"")
    await util.downloadImages(dlImgList, "")
    console.log("End")
}

/**
 * 取得一览
 * @param {返回的Html对象} $ 
 * @returns 
 */
function getListInfo($,folderNm) {
    console.log("开始取得一览信息")
    let dataPrimaryList = []
    // 标题
    let category = ""
    if (folderNm =="") {
        if(BASE_HOST.indexOf("eromanga")<0) {
            category = $("table").find("a")[0].children[0].data.replace(/ /,'').replace("/","")
            let folder = $("table").find("a")[1].children[0].data
            category = category + "/" + folder + "_" + $("time")[0].children[0].data.replace(/\./g,'')
        } else {
            category = $("div.date")[0].children[0].data.replace(/ /,'').replace(/\./g,'').trim()
        }
    } else {
        category = folderNm
    }
    console.log(category)
    let saveFolder = IMG_DIR + category
    util.createFolder(saveFolder)
    // 图片一览
    $("img").each((index, imgEle) => {
        // 存入集合
        let imgSrc = imgEle.attribs["src"]
        imgSrc = imgSrc.indexOf("http")<0 ? "https:" + imgSrc : imgSrc
        let imgNm = saveFolder + "/" + util.getSplitLast(imgSrc, '/', false)
        dataPrimaryList.push({ 'localNm': imgNm, 'netSrc': imgSrc, "downloadFlag": true, "overRadeFlag" : OVERRIDE_FLAG })
    })
    return dataPrimaryList
}
