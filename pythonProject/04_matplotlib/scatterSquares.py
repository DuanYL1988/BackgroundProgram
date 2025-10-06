# =============================================================
# 绘制散点图
# 1.matplotlib.plot()绘制连线
# 2.matplotlib.scatter()绘制点
# 3.使用matplotlib.savefig()保存图片前不能使用plt.show()
#   可以理解为plt对象表示一次后即会清空
# =============================================================
import commonUtil
import matplotlib.pyplot as plt


# 定义数列
baseValue = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
squares = []
for val in baseValue:
  if val < 0:
    val = 0 - val**2
  else:
    val = val**2

  squares.append(val)

# 散点图
#plt.scatter(baseValue,squares,s=10)

# 0-1000的平方曲线
x_value = list(range(1,1001))
y_value = [x**2 for x in x_value]

# edgecolor='none'删除点的轮廓
# c='red'设置点的颜色
#plt.scatter(x_value,y_value,c=(commonUtil.randomFloat(),commonUtil.randomFloat(),commonUtil.randomFloat()),edgecolor='none',s=2)

# 使用颜色映射: c=y_value,cmap=plt.cm.Blues
plt.scatter(x_value,y_value,c=y_value,cmap=plt.cm.Blues,edgecolor='none',s=2)

# 设置坐标轴取值范围
plt.axis([0,1100,0,1100000])

#plt.show()

# 保存图标,bbox_inches='tight' 去除多余空白
plt.savefig('square1-1000.png',bbox_inches='tight')
