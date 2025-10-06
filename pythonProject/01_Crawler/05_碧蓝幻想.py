import time
import CrawlerUtils
import copy

# 参数定义
defEnCode = "utf-8"
headers = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
BASE_NAME = "GRANBLUE_FANTASY"
BASE_URL = "https://gbf.huijiwiki.com/wiki/"
BASE_IMG_HOST = "https://huiji-public.huijistatic.com/gbf/uploads/"
RARITY_LIST = ["SSR人物","SR人物"]
MODEL_LIST = []
SKIN_LIST= {}
IMG_DIR = "../../htmlProject/00_illustration/05_GranblueFantasy/"
OVER_WRITT = False
# 模板
MODEL_TEMPLATE = {
  "no" : ""
  , "name" : ""
  , "title" : ""
  , "nameAttr" : ""
  , "category" : ""
  , "sex" : ""
  , "race" : ""
  , "faceImgSrc" : ""
  , "faceImg2" : ""
  , "illImgs" : ""
}

def getDataList():
  dataList = []
  for rarity in RARITY_LIST:
    # Step1. 通过URL取得dom对象
    doc = CrawlerUtils.getDomFromUrl(BASE_URL + rarity, '')
    for singleEle in doc.find_all("div",attrs= {'class':'flex-item char-box tabber-item'}):
      # 初始化对象
      model = copy.deepcopy(MODEL_TEMPLATE)
      # 解析Dom
      model["category"] = singleEle.get("data-category")
      model["sex"] = singleEle.get("data-gender")
      model["race"] = singleEle.get("data-race")
      img = singleEle.find("img")
      model["no"] = img.get("alt").split(" ")[1]
      model["faceImgSrc"] = getFaceImgUrl(img.get("src"))
      nameDiv = singleEle.find_all("a")[1]
      name = nameDiv.text
      if '<span' in name:
        name = nameDiv.text[0,name.index('<span')]
        name += nameDiv.find("span").text
      else:
        name = nameDiv.text
      model["nameAttr"] = name
      # 放入元组
      dataList.append(model)
  return dataList

def getDetail(MODEL_LIST):
  for model in MODEL_LIST:
    #if model["no"] == '3040278000' or model["no"] != "":
      detailUrl = BASE_URL + 'Char/' + model["no"]
      detail = CrawlerUtils.getDomFromUrl(detailUrl, 'detail.html')
      model["name"] = detail.find("div",attrs={"class":"character-item-name"}).text
      model["title"] = getTitleName(detail.find("div",attrs={"class":"character-evo-name jp"}).text)
      # 取得立绘集合
      model["illImgs"] = []
      for illImg in detail.find_all("div",attrs={'class':'character-zoom tabber-item'}):
        imgEle = illImg.find_all("img")
        if len(imgEle) > 0 :
          model["illImgs"].append(imgEle[0].get("src").replace(BASE_IMG_HOST,''))
      # 取得横向头像
      face2Ele = detail.find("img",attrs={"alt":model["nameAttr"],"title":model["nameAttr"]})
      if None != face2Ele:
        model["faceImg2"] = face2Ele.get("src").replace(BASE_IMG_HOST,'')
      editDownloadImages(model)
      CrawlerUtils.writeLine("./CrawlerDataFile", BASE_NAME, model)
      print("间隔10秒,做一个良性爬虫")

      time.sleep(10)

def editDownloadImages(model):
  folder = IMG_DIR + model["name"]+"_"+model["no"]
  CrawlerUtils.downloadImage(folder, "faceIcon", BASE_IMG_HOST + model["faceImgSrc"], OVER_WRITT)
  if "" != model["faceImg2"]:
    CrawlerUtils.downloadImage(folder, "faceIcon2", BASE_IMG_HOST + model["faceImg2"], OVER_WRITT)
  for illImg in model["illImgs"]:
    CrawlerUtils.downloadImage(folder, illImg[10:-4], BASE_IMG_HOST + illImg, OVER_WRITT)

'''
私有方法编辑区Start
'''
def getFaceImgUrl(imgSrc) :
  src01 = imgSrc.split('thumb/')[-1]
  return src01.split("/100")[0]

def getTitleName(str):
  if str.index('[') >= 0 and str.index(']') > 0 :
    return str[str.index('[')+1:str.index(']')]
  else :
    return str
'''
私有方法编辑区End
'''

# 取得一览
MODEL_LIST = getDataList()
# 取得详细
getDetail(MODEL_LIST)
# 输出结果
CrawlerUtils.outputJsonCsv('./CrawlerDataFile',BASE_NAME,MODEL_LIST)

print("End")
