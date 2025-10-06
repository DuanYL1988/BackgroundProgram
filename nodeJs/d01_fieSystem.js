const util = require('./resources/nodeCommon')

const PATH = "../00_illustration/01_feh/"
const DL_PATH = "C:\\Users\\dylsw\\OneDrive\\图片\\feTemp\\"
const NAMES = ["Ursula_Blackened_Crow"]

// copyFehImg()

/**
 * 将火纹英雄立绘拷贝到临时上传文件夹
 */
function copyFehImg(){
    console.log("Start")
    NAMES.forEach(async folderNm => {
        console.log("debug", folderNm)
        let fromPath = PATH + folderNm + "/01_normal.png"
        let toPath = DL_PATH + folderNm + "_1.png"
        await util.copyFile(fromPath, toPath, false)
        fromPath = PATH + folderNm + "/02_attact.png"
        toPath = DL_PATH + folderNm + "_2.png"
        await util.copyFile(fromPath, toPath, false)
        fromPath = PATH + folderNm + "/03_extra.png"
        toPath = DL_PATH + folderNm + "_3.png"
        await util.copyFile(fromPath, toPath, false)
        fromPath = PATH + folderNm + "/04_break.png"
        toPath = DL_PATH + folderNm + "_4.png"
        await util.copyFile(fromPath, toPath, false)
    })
    console.log("End")
}

//getFiles("D:\\休闲时光\\学习资料\\man hua\\Gif")
getFiles("D:\\休闲时光\\学习资料\\man hua\\世界樹の迷宮")

async function getFiles(baseFolder) {
    const fs = require('fs')
    let name = util.getSplitLast(baseFolder,"\\",false)
    let json = createModel(name, baseFolder)
    fs.readdir(baseFolder, (err, files) =>{
        if(err) {
            console.log("error", "读取文件出错")
        }
        // 判断是否是文件夹
        for(let i = 0; i < files.length ; i ++) {
            let file = files[i]
            let filePath = baseFolder + "\\" + file
            // let folderFlag = isFolder(filePath)
            json[name].pictures.push(file)
        }
        console.log(JSON.stringify(json))
    })
}

function isFolder(path){
    const fs = require('fs')
    fs.stat(path, (err, stats) => {
        if (err) {
            console.error('无法获取路径信息:', err);
            return false
          }
          // 检查路径是否是文件夹
          if (stats.isDirectory()) {
            console.log(`${path} 是一个文件夹。`);
            return true
          } else {
            console.log(`${path} 不是一个文件夹。`);
            return false
          }
    })
}

function createModel(name,path){
    let obj = {}
    obj[name] = {"path" : path, "pictures" : []}
    return obj
}

