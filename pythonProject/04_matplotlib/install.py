# =============================================================
# 安装matplotlib
# 1.cmd中进入项目所在文件夹
# >d:
# >cd D:\project\pythonObj\matplotlib
# >python -m pip install --user matplotlib-3.4.3-cp39-cp39-win_amd64.whl
# =============================================================
import matplotlib.pyplot as plt

# 绘制简单的折线图,计算平方
baseValue = [1,2,3,4,5]
squares = []
for val in baseValue:
  squares.append(val**2)

# 折线宽度
plt.plot(baseValue,squares,linewidth=5)

plt.title("Square Numbers",fontsize=24)
plt.xlabel("Value",fontsize=14)
plt.ylabel("Square of value",fontsize=14)

# 设置刻度标记
plt.tick_params(axis='both',labelsize=14)
plt.show()
