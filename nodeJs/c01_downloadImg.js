/** 通用导入部分 */
const util = require('./resources/nodeCommon')
// 爬取图片存放路径 
const IMG_DIR = "../00_illustration/04_GranblueFantasy/"
// 保存json文件
// 基本域名
const IMGSRC = "b/bf/Zoom_3040006000_01.png"
const IMG_HOST = "https://huiji-public.huijistatic.com/gbf/uploads/"

let downloadBox = [
    {"localNm" : IMG_DIR + "3040006000_01.png", "netSrc" : IMGSRC, "overRadeFlag" : true, "downloadFlag" : true}
]
util.downloadImages(downloadBox,IMG_HOST)