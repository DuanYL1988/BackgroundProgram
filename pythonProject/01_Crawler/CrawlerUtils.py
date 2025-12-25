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
  #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
# 访问间隔
SLEEP_TIME = 30

''' ======= 输出信息相关 ======== '''
def copyJson(jsonObj):
  pyperclip.copy(json.dumps(jsonObj, indent=2,ensure_ascii=False))
  print("JSON格式化并复制到剪切板!")

def printJson(jsonObj):
  jsonStr = json.dumps(jsonObj, indent=2,ensure_ascii=False)
  print(jsonStr)

def copyText(copyStr):
  pyperclip.copy(copyStr)

def googleTranslateEnToCn(searchWord):
  ''' ======= 谷歌翻译 ======== '''
  return GoogleTranslator(source='en', target='zh-CN').translate(searchWord)

def googleTranslate(searchWord, from_lang, to_lang):
  from_lang = 'en' if "" == from_lang else from_lang
  to_lang = 'zh-CN' if "" == to_lang else to_lang
  # 初始化翻译器
  translator = GoogleTranslator(source=from_lang, target=to_lang)
  # 需要翻译的文本
  text = searchWord
  # 翻译文本
  return translator.translate(text, src=from_lang, dest=to_lang)

def baiduTransEnToCn(searchWord):
  ''' 百度翻译  MD 每个月有字数限制 '''
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

def doGetText(url):
  ''' 默认编码以及参数请求 '''
  return doGetTextParam3(url, defEnCode, {})

def doGetTextOutput(url, outputPath):
  ''' Get请求取得文本信息并输出到文件 '''
  text = doGetText(url)
  if "" != outputPath:
    outputHtml(text, defEnCode, outputPath)
  return text

def doGetTextParam3(url, encode, params):
  ''' Get请求取得文本信息 '''
  resp = requests.get(url, params = params, headers = headers, impersonate="chrome101", timeout=10)
  resp.encoding = encode
  text = resp.text
  resp.close()
  return text

def doGetJson(url, encode, params):
  ''' Get请求取得Json信息 '''
  resp = requests.get(url, params = params, headers = headers, impersonate="chrome101", timeout=10)
  resp.encoding = encode
  json = resp.json()
  resp.close()
  return json

def doPost(url, encode, params):
  ''' Post请求 '''
  resp = requests.post(url, data = params, headers = headers, impersonate="chrome101", timeout=10)
  resp.encoding = encode
  json = resp.json()
  resp.close()
  return json

def transHtmlToDom(html_content):
  return BeautifulSoup(html_content, "html.parser")

def outputHtml(outputText, encode, fileName):
  '''  输出到文件 '''
  print(f"输出文件:{fileName}")
  with open(fileName, mode="w" , encoding=encode) as f:
    f.write(str(outputText))
  f.close()

def setRequetHeaders(customHeaders):
  ''' 设置请求头 '''
  for key in customHeaders:
    headers[key] = customHeaders[key]  

def getDataListByReg(html, patternStr):
  ''' 正则匹配数据 '''
  # 加载正则到内存
  pattern = re.compile(patternStr, re.S)
  dataList = []
  for item in pattern.finditer(html):
    dataList.append(item.groupdict())
  return dataList

def getDomFromUrl(url, outputPath):
  '''  通过url直接取得dom对象  '''
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

def getDomForHtml(html):
  ''' 通过html文字列取得dom对象'''
  return BeautifulSoup(html, "html.parser")

def getXpathForHtml(html, parentXpath):
  xpathObj = etree.HTML(html)
  return xpathObj.xpath(parentXpath)

def outputJsonCsv(outputPath, modalName, dataList):
  ''' 输出json和csv数据文件 '''
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

def writeLine(outputPath, modalName, jsonObj):
  ''' 写入json '''
  with open(f"{outputPath}/{modalName}.json", mode="a", encoding=defEnCode) as file:
    file.write("    " + str(jsonObj) + ",\n")
    file.close()

def formateJSON(data):
  ''' 格式化json '''
  return json.dumps(data, indent=4, ensure_ascii=False)

def matchStr(str,partten):
  ''' 正则匹配 '''
  match = re.match(partten, str)
  if match:
    str = ""
    for part in match.groups():
      str += part
  return str

def matchYMD(str,partten):
  ''' 正则匹配:转换年月日 '''
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

def downloadImage(forlder, name, src, overWriteFlag, pngFlag):
  ''' 下载图片 '''
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
    os.makedirs(forlder)
  with open(outputFileName, mode="wb") as f:
    f.write(img_resp.content)
    print(f"download:{src.split('/')[-1]} -> {outputFileName}")
    # 下载完成间隔时间
    time.sleep(2)

def getSrcFromTd(tdElement):
  ''' 从td中取得img的src '''
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

def initData(dataModel, regData):
  ''' 初始化对象并赋值 '''
  data = copy.deepcopy(dataModel)
  for attr in regData:
    data[attr] = regData[attr].strip()
  return data

if __name__ == "__main__":
  print("CrawlerUtils模块测试")