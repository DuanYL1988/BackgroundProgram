#====================================================
# 总结
# 1.添加元素 LIST.append(item)
# 2.直接删除元素 del LIST[index]
# 3.弹出元素 LIST.pop(),LIST.pop(index)
# 4.通过值直接删除 LIST.remove(string)
# 5.排序 List.sort(),List.sort(reverse=True)
#====================================================

# 定义列表的方式和js相似
colorList = ["red","orange","yellow","green","blue","gray","black"]
print(colorList[0])

# 添加元素,java:add(),python是append()
print("在末尾插入gold")
colorList.append("gold")
# 可以在任意位置插入 insert()
print("在第2位插入#fffff")
colorList.insert(1,"#fffff")
print(colorList)
print("\n")

# 删除元素,和添加不同,使用命令行而不是函数 del
del colorList[1]
print("直接删除第2位元素\n")
print(colorList)
print("\n")

# 去除最后元素并从列表中删除,对应了java中的两步操作
# 可以理解为取栈中第一个元素,队列中最后一个
# pop()指定下表可以去除任意位置的元素
firstItem = colorList.pop()
print("弹出队列中最后一位")
print(firstItem)
print(colorList)
print("\n")
targetItem = colorList.pop(2)
print("弹出任意下标")
print(targetItem)
print(colorList)
print("\n")

# python可以通过值直接删除,这点比java效率很多.使用remove()
iwantDelItem = "blue"
colorList.remove(iwantDelItem)
print("直接删除值是blue的元素")
print(colorList)
print("\n")

# 排序,排序不可逆
colorList.sort()
print(colorList)
print("倒叙排列.sort(reverse=True),注意True写法")
colorList.sort(reverse=True)
print(colorList)

# 列表长度 java.list.size() = python.len(list)
print(len(colorList))
