const mongoose = require('mongoose')
const Schema = require('./Schema.json')

const testData = { "no": "", "name": "Therese (Bunny)", "nameCN": "", "nameJP": "", "element": "Fire", "type": "Label Race Human", "race": "Label Type Balance", "weapon": "Sabre", "artImgs": ["2/22/ThereseBunny_A.png", "0/0a/ThereseBunny_B.png"], "sprites": ["1/11/ThereseBunny_SDA.png", "5/54/ThereseBunny_SDB.png"], "detailLink": "https://granblue.fandom.com/wiki/Therese_(Bunny)" }
const SERVER_URL = "mongodb://localhost:27017/admin"

/*
const docName = "granblue_fantasies"
main()
async function main(){
    console.log("Start")
    let conn = await getConnection()
    let updRst = await insetUpdateData(conn, docName, testData, {"name": "Zeta"})
    console.log(updRst)
    conn.disconnect()
}
*/

/**
 * 取得mongoDb链接
 * @returns mongoDb连接对象
 */
function getConnection() {
    return mongoose.connect(SERVER_URL)
}

/**
 * 取得数据
 * @param {mongoDb连接} conn 
 * @param {表名} docName 
 * @param {条件} condition 
 * @returns 检索结果
 */
async function getData(conn, docName, condition) {
    // conn.model不是异步函数
    let findModel =  conn.model(docName, Schema[docName])
    // 操作DB是异步
    let result = await findModel.find(condition)
    return result
}

/**
 * 取得数据<br>
 * 只连接一次, 不需要提供mongoDb连接
 * @param {表名} docName 
 * @param {条件} condition 
 * @returns 检索结果
 */
async function getDataOnce(docName, condition) {
    let conn = await getConnection()
    // conn.model不是异步函数
    let findModel =  conn.model(docName, Schema[docName])
    // 操作DB是异步
    let result = await findModel.find(condition)
    conn.disconnect()
    return result
}

async function getDataHasModel(model, condition, findOneFlag){
    let result = await model.find(condition)
    if (findOneFlag && result.length > 0) {
        result = result[0]
    }
    return result
}

/**
 * 登录或更新一条数据
 * 请确认复合条件的数据小于1条
 * @param {mongoDb连接} conn 
 * @param {表名} docName 
 * @param {登录的数据} registData 
 * @param {条件} condition 
 * @returns 
 */
async function insetUpdateData(docModel, registData, condition) {
    let findDt = await docModel.find(condition)
    let result = ""
    if (findDt.length == 1) {
        result = await docModel.updateOne(condition, registData)
    } else if (findDt.length > 1){
        await docModel.deleteOne(condition)
        result = await docModel.create(registData)
    } else {
        result = await docModel.create(registData)
    }
    return result
}

module.exports = {
    getConnection
    , getData
    , getDataOnce
    , getDataHasModel
    , insetUpdateData
}