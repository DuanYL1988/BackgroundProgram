/** 通用导入部分 */
const util = require('./resources/nodeCommon')
const dbUtil = require('./resources/mongoDb')
const Schema = require('./resources/Schema.json')
// 爬取图片存放路径 
const IMG_DIR = "D:\\picture\\"
const FOLDER = "火灵儿3D"
// 持久化相关
const DL_FLAG = false
const OVERRIDE_FLAG = false


getDetail()

async function getDetail() {
    const link = "https://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_4340990422495856770"
    const $ = await util.getTargetElementByAxios(link, "", "templateList.html", true)

    console.log("end")
}
