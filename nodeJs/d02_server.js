const util = require('./resources/common/nodeCommon')
// 导入http模块
const http = require('http')

// 创建服务对象
const server = http.createServer((request, response) => {
    // 请求
    let requestType = request.method
    let url = "." + request.url
    console.log(url)
    if (url.indexOf('.css') > 0 || url.indexOf('.js') > 0) {
        response.end(util.readFile(url))
    } else if(url.indexOf('.png') > 0 || url.indexOf('.jpg') > 0 
        || url.indexOf('.gif') > 0 || url.indexOf('.webp') > 0){
            // TODO /00_illustration/03_碧蓝航线/Reno/Reno.png
            response.end(util.readFile('./00_illustration/03_碧蓝航线/Reno/Reno.png'))
    } else {
        // 响应
        response.setHeader('content-type', 'text/html;charset=utf-8')
        let path = url.indexOf(".html") > 0 ? url.split("?")[0] : "./login.html"
        let html = util.readFile(path)
        response.end(html.toString())
    }


})

// 3. 监听端口,启动服务
server.listen(9000, () => {
    console.log('服务已经启动')
})

function parseGetParam(url) {
    let requestObj = {}

    let paramStr = url.replace('/?', '')
    paramStr.split('&').forEach(param => {
        let info = param.split('=')
        requestObj[info[0]] = info[1]
    })
    return requestObj
}