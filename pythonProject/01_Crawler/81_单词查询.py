import argparse
import CrawlerUtils
import copy
import DBUtil

# 数据模型
DATA_MODEL = {
    "WORD_EN" : "" # 单词_英文
    , "WORD_CN" : "" # 单词_中文
    , "WORD_JP" : "" # 单词_日文
    , "WORD_TYPE" : "" # 单词类型
}

def translateWord(word):
    wordCn = CrawlerUtils.googleTranslateEnToCn(word)
    wordJp = CrawlerUtils.googleTranslate(word, "en", "ja")
    print(f"{word} 的翻译是: {wordCn}")
    dataObj = copy.deepcopy(DATA_MODEL)
    dataObj["WORD_EN"] = word
    dataObj["WORD_CN"] = wordCn
    dataObj["WORD_JP"] = wordJp
    dataObj["WORD_TYPE"] = "技术文档"  # You can set the word type here if needed
    # 插入数据库
    print(dataObj)
    DBUtil.doInsertByKey("WORD_TRANS", dataObj, {"WORD_EN":word})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="单词翻译")
    word = input("请输入需要翻译的单词:")
    translateWord(word.strip())

