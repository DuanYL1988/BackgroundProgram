// 文件操作, 导入fs
const fs = require('fs')
const moment = require('moment')
const path = require('path')
const axios = require('axios')
const rp = require('request-promise');
const cheerio = require('cheerio')

// 请求头
const config = {
    headers : {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
}

/** 
 * 使用流写入文件
 * @Param  {文件地址} filePath
 * @Param  {写入内容} data
 */
async function writeFileWithStream(filePath, data) {
    var ws = fs.createWriteStream(filePath)
    // 写入内容
    if ("object" === typeof data) {
        ws.write(JSON.stringify(data))
    } else {
        ws.write(data)
    }
    // 关闭流
    ws.close()
}

/** 
 * 写入文件
 * @Param  {文件地址} filePath
 * @Param  {写入内容} data
 */
async function writeFile(filePath, data) {
    await fs.writeFileSync(filePath, data, err => {
        if (err) {
            console.error("error", "写入失败!")
            return
        }
        console.log(filePath + "写入完成")
    })
}

/** 
 * 文件追加写入内容
 * @Param  {文件地址} filePath
 * @Param  {写入内容} data
 */
async function addText(filePath, data) {
    fs.appendFileSync(filePath, data, err => {
        if (err) {
            console.error("error", "追加内容写入失败!")
            return
        }
        console.info("info", "追加内容写入成功!")
    })
}

/** 
 * 读取文件
 * @Param  {文件地址} filePath
 */
function readFile(filePath) {
    let data = fs.readFileSync(filePath)
    return data
}

/** 
 * 读取文件
 * @Param  {文件地址} filePath
 */
function readFileStream(filePath) {
    let rs = fs.readFileStream(filePath)
    rs.on('data', chunk => {

    })
    rs.on('end', chunk => {

    })
}

/**
 * 删除文件
 * @param {文件地址} filePath 
 */
async function deleteFile(filePath) {
    try {
        fs.unlinkSync(filePath)
    } catch (e) {
        console.error("文件不存在")
    }
}

/** 
 * 取得文件基本信息
 * @Param  {文件地址} filePath
 */
function getFileStatus(filePath) {

    if (!fs.existsSync(filePath)) {
        return null
    }
    let fileInfo = path.parse(filePath)

    // 取得资源状态
    fs.statSync(filePath, (err, data) => {
        if (err) {
            console.log("文件读取失败")
        }
        fileInfo["isFile"] = data.isFile()
        fileInfo["isFolder"] = data.isDirectory()
    })
    return fileInfo
}

/** 
 * 拷贝文件
 * @Param {拷贝原文件地址} originFile
 * @Param {拷贝文件名} copyTarget
 * @Param {是否删除原文件} deleteFlag
 */
async function copyFile(originFile, copyTarget, deleteFlag) {
    let rs = fs.createReadStream(originFile)
    let ws = fs.createWriteStream(copyTarget)
    rs.on('data', chunk => {
        ws.write(chunk);
    })

    rs.on('end', () => {
        console.log("文件复制完毕!")
        ws.close()
        if (deleteFlag) {
            fs.unlinkSync(originFile)
        }
    })
}

/** 
 * 创建文件夹
 * @Param {文件夹路径} path
 */
async function createFolder(path) {
    if (fs.existsSync(path)) {
        return
    }
    fs.mkdirSync(path, { recursive: true }, err => {
        if (err) {
            console.error("error", "文件夹创建失败")
        }
    })
    console.error("info", path + "文件夹创建成功")
}

/**
 * 使用request请求连接取得需要的element.
 * @param {网页链接} linkUrl 
 * @param {jquery选择器} selector 
 * @param {结果输出文件} outputFile 
 * @param {是否输出结果} outputFlag 
 * @returns 
 */
async function getElementByRequest(linkUrl, selector, outputFile, outputFlag, index) {
    // 没传文件名 不进行输出
    outputFlag = isEmpty(outputFile) ? false : outputFlag
    // 没设开关 默认不输出
    outputFlag = isEmpty(outputFlag) ? false : outputFlag
    index = isEmpty(index) ? 0 : index
    let options = {
        method: 'GET',
        uri: linkUrl,
        json: true // 自动解析JSON
    }
    var result = await rp(options).then(response => {
        var $ = cheerio.load(response)
        // 截取显示图片的区域DIV
        if (!isEmpty(selector)) {
            if ($("html").find(selector).length == 1) {
                $ = cheerio.load($("html").find(selector)[index])
            } else {
                let tag = selector.split(".")[0]
                let html = "<html><body>"
                $(selector).each((index, element)=>{
                    if(index == 0) {
                        html += "<" + tag +">"
                    }
                    html += $(element).html()
                })
                html += "</" + tag +">" + "</body></html>"
                $ = cheerio.load(html)
            }
        }
        if (outputFlag) {
            writeFile(outputFile, $.html())
        }
        return $
    }).catch(err => {
        console.error('发生错误:', err.statusCode);
        throw err
    });
    return result
}

/**
 * 使用axios请求连接取得需要的element.
 * @param {网页链接} linkUrl 
 * @param {jquery选择器} selector 
 * @param {结果输出文件} outputFile 
 * @param {是否输出结果} outputFlag 
 * @param {第n个元素} index 
 * @returns 
 */
async function getTargetElementByAxios(linkUrl, selector, outputFile, outputFlag, index) {
    // 没传文件名 不进行输出
    outputFlag = isEmpty(outputFile) ? false : outputFlag
    // 没设开关 默认不输出
    outputFlag = isEmpty(outputFlag) ? false : outputFlag
    //
    index = isEmpty(index) ? 0 : index
    try {
        // 用axios取得response
        const {data} = await axios.get(linkUrl, config)
        // 使用cheerio转为类似jquery的document对象
        var $ = cheerio.load(data)
        // 截取显示图片的区域DIV
        if (!isEmpty(selector)) {
            $ = cheerio.load($("html").find(selector)[index])
        }
        if (outputFlag) {
            await writeFile(outputFile, $.html())
        }
        return $
    } catch (error) {
        writeErrorLog(linkUrl + " error code : " + error, 'nodeCommon.js', 'getTargetElementByRequest')
        return "error"
    }
}

function loadHtml() {

}

function getColHtml(tdElement){
    let childrenElements = tdElement.children
    if(childrenElements.length == 1){
        let childEle = childrenElements[0]
        if('text' == childEle.type) {
            return childEle.data
        } else if('tag' == childEle.type) {
            return childEle.children[0].data
        }
    }
}

/** 
 * 从路径取得文件名
 * @Param {图片路径} imgPath
 */
function getNameFromPath(imgPath) {
    try {
        let imgNameArr = imgPath.split("/")
        return imgNameArr[imgNameArr.length - 1]
    } catch (error) {
        writeErrorLog(error, 'nodeCommon.js', 'getNameFromPath')
    }
}

/**
 * 批量下载图片
 * @param {下载图片集合} imgBox 
 * @param {图片服务器地址} imgHost 
 */
async function downloadImages(imgBox, imgHost) {
    for (let i = 0; i < imgBox.length; i++) {
        let dlObj = imgBox[i]
        if (dlObj.downloadFlag) {
            await downloadSingleImage(dlObj["localNm"], imgHost + dlObj["netSrc"], dlObj.overRadeFlag)
        }
    }
}

/** 
 * 从路径取得文件名
 * @Param {图片路径} dlPath
 * @Param {网络URL} imgSrc
 * @Param {是否覆盖 true:覆盖,false:不覆盖} overRadeFlag
 */
async function downloadSingleImage(dlPath, imgSrc, overRadeFlag) {
    overRadeFlag = isEmpty(overRadeFlag) ? false : overRadeFlag
    // 文件存在且不覆盖, 返回
    if (fs.existsSync(dlPath) && !overRadeFlag || typeof(overRadeFlag)=="undefined") {
        console.info("->file existed : " + dlPath)
    } else {
        // 扩展名
        let imgName = getSplitLast(dlPath, '/', false)
        if (imgName.indexOf(".") < 0) {
            let fileEx = getSplitLast(imgSrc, '/', false)
            fileEx = getSplitLast(fileEx, '.', true)
            imgName = imgName + fileEx
            dlPath = dlPath + fileEx
        }
        console.info("Start Download : " + imgSrc + " -> " + dlPath)
        try {
            await axios.get(imgSrc, { responseType: 'arraybuffer' }).then(res => {
                if (res.status === 200) {
                    fs.writeFile(dlPath, res.data, 'binary', (err) => {
                        if (!err) {
                            console.info("->download image : " + imgName + " success!")
                        }
                    })
                } else {
                    let msg = "#" + dlPath + "#," + imgSrc + ", status : " + res.status
                    writeErrorLog(msg, 'nodeCommon.js', 'downloadSingleImage')
                }
            })
            return "success"
        } catch (error) {
            let msg = "#" + dlPath + "#," + ": " + dlPath + "," + imgSrc + "," + error
            writeErrorLog(msg, 'nodeCommon.js', 'downloadSingleImage')
        }
    }
}

// /revision
function replaceNetImgUrl(src, cutHost) {
    let fileExArr = [".webp", ".png", ".jpg", ".jpeg", ".gif", ".WEBP", ".PNG", ".JPG", ".JPEG", ".GIF"]
    fileExArr.forEach(exNm => {
        if (src.indexOf(exNm) > 0) {
            let srcPart = src.split(exNm)
            src = srcPart[0] + exNm
        }
    })
    if (!isEmpty(cutHost)) {
        src = src.split(cutHost)[1]
    }
    return src
}

function isEmpty(obj) {
    if (null == obj || 'undefined' == obj) {
        return true
    } else if (typeof(obj) == 'string' && '' == obj) {
        return true
    }
    return false
}

/**
 * 取得tag的内容, Param2中只有一个tag时使用
 * @param {doc文档} $ 
 * @param {总内容} str 
 * @param {提取的标签} tagNm 
 * @returns 标签的jquery对象
 */
function getTagElement($, str, tagNm) {
    // 结束标签
    let endTg = "</" + tagNm + ">"
    // 结束标签前的内容
    str = str.split(endTg)[0] + endTg
    // 开始标签
    let stTg = "<" + tagNm + ">"
    // 开始标签是否有是<tag>形式 <tag attr=...
    stTg = str.indexOf(stTg) >= 0 ? stTg : stTg.replace('>', ' ')
    // 开始标签后的内容
    str = stTg + str.split(stTg)[1]
    return $(str)
}

function getCurrDt(ptn) {
    ptn = isEmpty(ptn) ? 'YYYY-MM-DD HH:mm:ss' : ptn
    const date = moment();
    const formattedDate = date.format(ptn);
    return formattedDate
}

/**
 * 登录错误日志
 * @param {错误信息} errText 
 * @param {文件名} fileNm 
 * @param {方法名} methodNm 
 */
function writeErrorLog(errText, fileNm, methodNm) {
    let dt = getCurrDt()
    errText = 'object' == typeof errText ? JSON.stringify(errText) : errText
    addText('./error.log', dt + ' : [' + fileNm + '][' + methodNm + '] ' + errText + "\r\n")
}

/**
 * 登录消息日志
 * @param {信息} errText 
 * @param {文件名} fileNm 
 * @param {方法名} methodNm 
 */
function writeInfoLog(infoText, fileNm, methodNm) {
    let dt = getCurrDt()
    infoText = 'object' == typeof infoText ? JSON.stringify(infoText) : infoText
    addText('./info.log', dt + ' : [' + fileNm + '] ' + infoText + "\r\n")
}

async function saveJson(jsonData, jsonFile, lastLineFlag) {
    let text = "object" == typeof jsonData ? "    " + JSON.stringify(jsonData) : jsonData
    if("object" == typeof jsonData) {
        if (lastLineFlag) {
            text += "\r\n]"
        } else {
            text += ","
        }
    }
    addText(jsonFile, text + "\r\n")
}

/**
 * 取得分割最后字符串
 * @param {文字列} str 
 * @param {分隔符} splitStr 
 * @param {结尾是否包含分隔符} withSplit 
 * @returns 
 */
function getSplitLast(str, splitStr, withSplit) {
    let arr = str.split(splitStr)
    let result = withSplit ? splitStr + arr[arr.length - 1] : arr[arr.length - 1]
    return result
}

/**
 * 将list转为散列表
 * @param {集合} list 
 * @param {分组属性} keyAttr 
 * @returns 
 */
function transListToMap(list, keyAttr) {
    let resultMap = {}
    for (let i = 0; i < list.length; i++) {
        let currentData = list[i]
        let key = currentData
        if(!isEmpty(keyAttr)) {
            let key = currentData[keyAttr].replace(/_/g, '')
            resultMap[key] = currentData
        } else {
            resultMap[key] = "-"
        }
    }
    return resultMap
}

/**
 * 将网络图片地址分割为[host , 图片名]
 * @param {网络图片地址} imgSrc 
 * @returns 
 */
function splitWebImgSrc(imgSrc) {
    let netUrlReg = new RegExp(/[0-9a-fA-F]{1,2}\/[0-9a-fA-F]{1,2}\//)
    let splitResult = imgSrc.split(netUrlReg)
    return {"imgHost" : splitResult[0], "imgName" : splitResult[splitResult.length-1], "splitStr" : netUrlReg.exec(imgSrc)[0]}
}

module.exports = {
    writeFile
    , writeFileWithStream
    , addText
    , getFileStatus
    , readFile
    , readFileStream
    , copyFile
    , deleteFile
    , createFolder
    , getElementByRequest
    , getTargetElementByAxios
    , getNameFromPath
    , downloadImages
    , downloadSingleImage
    , replaceNetImgUrl
    , isEmpty
    , getCurrDt
    , writeErrorLog
    , writeInfoLog
    , saveJson
    , getSplitLast
    , getTagElement
    , transListToMap
    , splitWebImgSrc
    , getColHtml
}

