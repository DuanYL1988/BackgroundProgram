# 需安装第三方库
# pip install curl_cffi
from curl_cffi import requests
# 引入正则模块
import re
# 使用BS4解析html, 安装 pip install bs4
from bs4 import BeautifulSoup
# 解析URL
import urllib.parse
import json
# 使用Xpath解析数据 安装 pip install lxml 
from lxml import etree
# 引入CSV
import os
import csv
import time
import random
from hashlib import md5
#
import copy
# 安装 googletrans 库
# pip install googletrans==4.0.0-rc1
# python 3.11之后版本一处cgi模块无法使用
# from googletrans import Translator
# pip install deep-translator
from deep_translator import GoogleTranslator
# 复制内容到内存
# pip install pyperclip
import pyperclip

# 参数定义
defEnCode = "utf-8"
headers = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
# 访问间隔
SLEEP_TIME = 30

''' ======= 输出信息相关 ======== '''
def copyJson(jsonObj):
  pyperclip.copy(json.dumps(jsonObj, indent=2))
  print("JSON格式化并复制到剪切板!")

def printJson(jsonObj):
  jsonStr = json.dumps(jsonObj, indent=2)
  print(jsonStr)

def copyText(copyStr):
  pyperclip.copy(copyStr)

''' ======= 谷歌翻译 ======== '''
def googleTranslateEnToCn(searchWord):
  #return googleTranslate(searchWord, 'en', "zh-cn")
  return GoogleTranslator(source='auto', target='zh').translate(searchWord)

def googleTranslate(searchWord, from_lang, to_lang):
  from_lang = 'en' if "" == from_lang else from_lang
  to_lang = 'zh-cn' if "" == to_lang else from_lang
  # 初始化翻译器
  translator = Translator()
  # 需要翻译的文本
  text = searchWord
  # 翻译文本
  translation = translator.translate(text, src=from_lang, dest=to_lang)
  # 显示翻译结果
  return f'{translation.text}'

'''
百度翻译
MD 每个月有字数限制
'''
def baiduTransEnToCn(searchWord):
  return baiduTranslate(searchWord, "auto", "cn")

def baiduTranslate(searchWord, from_lang, to_lang):
  # 设置你的appid和appkey
  appid = '20250304002292039'
  appkey = 'fv69lgIf_9CxJxLiHui3'
  # 翻译的源语言和目标语言
  from_lang = 'auto' if "" == from_lang else from_lang
  to_lang = 'zh' if "" == to_lang else from_lang
  # 百度翻译API的URL
  url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
  # 需要翻译的文本
  query = searchWord
  salt = random.randint(32768, 65536)
  # 生成随机数和签名
  s = appid + query + str(salt) + appkey
  sign = md5(s.encode(defEnCode)).hexdigest()
  # 构建请求参数
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  payload = {
      'appid': appid,
      'q': query,
      'from': from_lang,
      'to': to_lang,
      'salt': salt,
      'sign': sign
  }
  # 发送请求并获取响应
  response = requests.post(url, params=payload, headers=headers)
  result = response.json()
  # 显示翻译结果
  return result["trans_result"][0]["dst"]

'''
默认编码以及参数请求 
'''
def doGetText(url):
  return doGetTextParam3(url, defEnCode, {})

'''
Get请求取得文本信息
'''
def doGetTextParam3(url, encode, params):
  resp = requests.get(url, params = params, headers = headers, impersonate="chrome101", timeout=10)
  resp.encoding = encode
  text = resp.text
  resp.close()
  return text
'''
Get请求取得Json信息
'''
def doGetJson(url, encode, params):
  resp = requests.get(url, params = params, headers = headers, impersonate="chrome101", timeout=10)
  resp.encoding = encode
  json = resp.json()
  resp.close()
  return json

'''
Post请求
'''
def doPost(url, encode, params):
  resp = requests.post(url, data = params, headers = headers, impersonate="chrome101", timeout=10)
  resp.encoding = encode
  json = resp.json()
  resp.close()
  return json

'''
输出到文件
'''
def outputHtml(outputText, encode, fileName):
  with open(fileName, mode="w" , encoding=encode) as f:
    f.write(str(outputText))
  f.close()

'''
正则匹配
'''
def getDataListByReg(html, patternStr):
  # 加载正则到内存
  pattern = re.compile(patternStr, re.S)
  dataList = []
  for item in pattern.finditer(html):
    dataList.append(item.groupdict())
  return dataList

'''
通过url直接取得dom对象
'''
def getDomFromUrl(url, outputPath):
  respText = doGetText(url)
  if "" != outputPath:
    outputHtml(respText, defEnCode, outputPath)
  return getDomForHtml(respText)

def getDomFromUrlByCondition(url, tag, condition, outputPath):
  html = doGetText(url)
  doc = BeautifulSoup(html, "html.parser")
  targetElement = doc.find(tag, condition)
  if "" != outputPath:
    outputHtml(targetElement, defEnCode, outputPath)
  return targetElement

'''
通过html文字列取得dom对象
'''
def getDomForHtml(html):
  return BeautifulSoup(html, "html.parser")

def getXpathForHtml(html, parentXpath):
  xpathObj = etree.HTML(html)
  return xpathObj.xpath(parentXpath)

'''
输出json和csv数据文件
'''
def outputJsonCsv(outputPath, modalName, dataList):
  # 输出json格式
  outputJson = "const DATA_LIST = [\n"
  # 输出CSV格式
  csvFile = open(f"{outputPath}/{modalName}.csv", mode="w", newline="", encoding=defEnCode)
  csvwrite = csv.writer(csvFile)
  for item in dataList:
    csvwrite.writerow(item.values())
    outputJson += "    " + str(item) + ",\n"
  outputJson += "]"
  # 输出json文件
  outputHtml(outputJson, defEnCode, f"{outputPath}/{modalName}.json")
  csvFile.close()

'''
写入json
'''
def writeLine(outputPath, modalName, jsonObj):
  with open(f"{outputPath}/{modalName}.json", mode="a", encoding=defEnCode) as file:
    file.write("    " + str(jsonObj) + ",\n")
    file.close()

'''
格式化json
'''
def formateJSON(data):
  return json.dumps(data, indent=4, ensure_ascii=False)

'''
正则匹配
'''
def matchStr(str,partten):
  match = re.match(partten, str)
  if match:
    str = ""
    for part in match.groups():
      str += part
  return str

'''
正则匹配:转换年月日
'''
def matchYMD(str,partten):
  match = re.match(partten, str)
  if match:
    year, month, day = match.groups()
    str = f"{year}{int(month):02d}{int(day):02d}"
  return str

def splitByReg(str, partten):
  parts = re.split(partten, str)
  dataDir = {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}
  return dataDir

def matchWeapon(str):
  # 正则表达式模式：匹配英文字母、数字和加号
  pattern = r'[a-zA-Z0-9_ ]'
  matches = "".join(re.findall(pattern, str))
  return matches


def matchHp(text):
  result = ""
  text = text.replace(",","")
  text = text.replace(" / ","/")
  match = re.search(r'\b\d{3,5}/\d{3,5}\b', text)
  if match:
    result = match.group()
  return result

'''
下载图片
'''
def downloadImage(forlder, name, src, overWriteFlag, pngFlag):
  src = src.replace("'","")
  # 取得网络图片
  img_resp = requests.get(src, headers=headers)
  # 扩展名
  extName = src.split(".")[-1]
  if pngFlag:
    extName = "png" if "webp" == extName else extName
  outputFileName = forlder + name + "." + extName
  # 不覆盖
  if os.path.exists(outputFileName) and overWriteFlag == False:
    print("文件已存在,不覆盖,结束!")
    return
  # 没有文件夹时新建
  if not os.path.exists(forlder):
    os.mkdir(forlder)
  with open(outputFileName, mode="wb") as f:
    f.write(img_resp.content)
    print(f"download:{src.split("/")[-1]} -> {outputFileName}")
    # 下载完成间隔时间
    time.sleep(2)

'''
从td中取得img的src
'''
def getSrcFromTd(tdElement):
  imgElement = tdElement.find("img")
  return getSrcFromImgElement(imgElement)

def getSrcFromImgElement(imgElement):
  src = imgElement.get("data-src")
  if src is None:
    src = imgElement.get("src")
  parsed_url = urllib.parse.urlparse(src)
  file_extension = re.search(r'\.([a-zA-Z]+)',parsed_url.path).group(1)
  full_path = src.split(file_extension)[0]+file_extension
  src = "/".join(full_path.split("/")[-3:])
  return src

'''
初始化对象并赋值
'''
def initData(dataModel, regData):
  data = copy.deepcopy(dataModel)
  for attr in regData:
    data[attr] = regData[attr].strip()
  return data

'''
galleryHtml = BeautifulSoup(requests.get('https://azurlane.koumakan.jp/wiki/New_Jersey/Gallery'), "html.parser")
for imgLink in galleryHtml.find_all("img"):
    print(imgLink.get("src"))

# 使用DOM方式爬取数据
# 中文碧蓝航线wiki
baseUrl = 'https://wiki.biligame.com/'
listUrl = 'blhx/%E8%88%B0%E8%88%B9%E5%9B%BE%E9%89%B4'
parentNode = {"tag":"div","attrs":{"id","CardSelectTr"}}
childNode = {"tag":"div","attrs":{"class","jntj-1 divsort"}}
baseImgHost = "https://patchwiki.biligame.com/images/blhx/thumb"
getDataListByDom(baseUrl,listUrl,parentNode,childNode)
'''

'''
# 使用正则方式爬取数据
# 明日方舟
pattern = (r'<tr class="divsort" data-param1="(?P<type>.*?)" data-param2=".*?" data-param3="(?P<sex>.*?)" data-param4="(?P<group>.*?)" '
           r'data-param5="(?P<tag>.*?)".*?<a href="(?P<link>.*?)" title="(?P<name>.*?)".*?src="(?P<imgSrc>.*?)",*?')
getDataListByUrl("https://wiki.biligame.com", "arknights", pattern, "https://patchwiki.biligame.com/images/arknights/thumb/")
def getDataListByUrl(baseUrl, modalName, pattern, baseImgHost):
  html = doGetText(baseUrl + "/arknights/%E5%B9%B2%E5%91%98%E6%95%B0%E6%8D%AE%E8%A1%A8", defEnCode, {})
  getDataListByReg(html, pattern, baseImgHost, modalName)
  print("输出json文件结束!")

使用DOM方式解析
def getDataListByDom(baseUrl, listUrl, parentNode, childNode):
  # 1.将html交给BeautifulSoup进行处理,生成bs4对象
  page = getDomForHtml(doGetText(baseUrl + listUrl,defEnCode,{})) # 指定html解析器
  # 2.从bs对象中查找数据(find(标签,属性名),find_all)
  parent = page.find(parentNode["tag"], parentNode["attrs"])
  modelList = []
  for item in parent.find_all(childNode["tag"], childNode["attrs"]):
    model = {}
    imgEle = item.find("img")
    detailHtml = BeautifulSoup(doGetText(baseUrl + item.find("a").get("href"),defEnCode,{}), "html.parser")
    model["id"] = detailHtml.find("span",id="PNN").text
    model["name"] = imgEle.get("alt").replace("头像.jpg","")
    model["country"] = item.get("data-param3")
    model["rarity"] = detailHtml.find("span",id="PNrarity").text
    model["ship"] = detailHtml.find("span",id="PNshiptype").text
    model["releaseDate"] = detailHtml.find("table",class_="wikitable sv-general").find_all("tr")[3].find_all("td")[1].text.replace("\n","")
    downloadImage("./azurlane",model["name"],imgEle.get("src"))
    print(model)
    modelList.append(model)
    print("rest 5 second")
    time.sleep(SLEEP_TIME)
  outputJsonCsv("azurlane", modelList)

1.字符集
outputHtml(doGetText("https://pvp.qq.com/web201605/herolist.shtml","gbk", {}), defEnCode, "honorKing.html")

3.XHR->get请求传入参数
params = {
  "type": "24",
  "interval_id": "100:90",
  "action": "",
  "start": 0,
  "limit": 400
}
outputHtml(doGetJson("https://movie.douban.com/j/chart/top_list", defEnCode, params), defEnCode, "./豆瓣电影排行.json")

def getDataListByXpath(baseUrl):
  rows = getXpathForHtml(doGetText(baseUrl), '//*[@id="mw-content-text"]/div[1]/table/tbody/tr')
  modelList = []
  for tr in rows :
    if len(tr.xpath('./td[1]/a/text()')) > 0:
      model = {} 
      model["no"] = tr.xpath('./td[1]/a/text()')[0]
      model["name"] = tr.xpath('./td[1]/a/@title')[0]
      model["link"] = tr.xpath('./td[1]/a/@href')[0]
      model["rarity"] = tr.xpath('./td[3]/text()')[0]
      modelList.append(model)
  print(modelList)
'''
