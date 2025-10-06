const util = require('./resources/nodeCommon')

// util.replaceNetImgUrl(netSrc, 'images/')
// -> b/b7/Img_20190202_01-11.jpg



let data = {
    netSrc : "https://static.wikia.nocookie.net/feheroes_gamepedia_en/images/b/b7/Img_20190202_01-11.jpg/revision/latest?cb=20190202042928"
    , name : "肴·冬至"
}

let data2 = {}

console.debug(util.replaceNetImgUrl(data.netSrc, 'images/'))
console.debug(data.name.replace('·','_'))
console.debug(Object.keys(data))
