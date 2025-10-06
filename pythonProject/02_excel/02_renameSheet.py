# 导入xlwings组件
import xlwings as xw
import os

app = xw.App(visible=True, add_book=False)

path = "."
exName = ".xlsx"
for file in os.listdir(path):
  if(file.endswith(exName)):
    workbook = app.books.open(file)
    for sheet in workbook.sheets:
      sheet.name = sheet.name.replace("TBL_","")
    workbook.save()
app.quit()
