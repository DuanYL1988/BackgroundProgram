# 取得文件列表
# 导入OS模块
import os

path = "D:\\Project\\htmlProject\\00_illustration\\03_Azurlane"

for files in os.listdir(path):
  print(files)
