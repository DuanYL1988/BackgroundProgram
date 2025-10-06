from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 设置浏览器选项
'''
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面
chrome_options.add_argument("--disable-gpu")
'''

# 初始化 WebDriver
service = Service('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')  # 替换为你的 chromedriver 路径
driver = webdriver.Chrome(service=service)

try:
    # 打开目标网页
    driver.get("https://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88")

    # 等待页面加载，直到某个元素出现（例如页面的某个表格）
    wait = WebDriverWait(driver, 10)  # 最多等待 10 秒
    table = wait.until(EC.presence_of_element_located((By.ID, "result")))

    # 输出表格内容
    print("表格内容:")
    print(table.text)
finally:
    # 关闭浏览器
    driver.quit()
