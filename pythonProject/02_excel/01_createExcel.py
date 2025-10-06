# 导入xlwings组件
import xlwings as xw

app = xw.App(visible=True, add_book=False)

for tableName in ["FIEREMBLEM_HEROS","FATE_GRAND_ORDER", "AZURLANE", "GRANBLUE_FANTASY", "GENSHIN", "SNOW_BREAK", "HONOR_KINGS"]:
  workbook = app.books.add()
  workbook.save(f"./TBL_{tableName}.xlsx")
