# 1. 循环语法 for classnm in servantClassList :
# 2. 循环体内需要缩进(可以是一个空格),这块没有java严谨
# 3. 使用函数是看不到系统描述(类似于javadoc的东西)

# 循环写法类似于java  for (String nm : List)即执行循环又定义当前循环变量,注意句尾冒号
# 循环体内需要缩进,结束后处理删除缩进
# 由于没有括号保卫,这块很容易出现语法问题,需要特别注意
servantClassList = ['SABER','ARCHER','LANCER','RIDER','CASTER','ASSASSIN','BERSERKER']
print("每行都输出end")

existFlag = False
for classnm in servantClassList :
    # 判断句尾需要[:],不写();true和false作物布尔型首字母大写
    if "Avenger" not in servantClassList and existFlag != True :
        servantClassList.append("Avenger")
        existFlag = True
    # else if语法为 elif
    elif "AlterEgo" not in servantClassList :
        servantClassList.append("AlterEgo")
    else:
        print(classnm)

print(servantClassList)

print("\n循环结束后输入end")
for classnm in servantClassList :
    print(classnm)
print("end")

# 生成数字数组:range(START NUM,END NUM,STEP)STEP不设定默认为1
numList = list(range(1,11,3))
print(numList)

# 生成1-100,平计算总和
numList = list(range(1,101))
print(sum(numList))

squares = [val ** 2 for val in range(1,11)]
print(squares)

# 切片,截取数组 list[startIndex:endIndex],默认为0和最后一位
print(numList[2:4])
print(numList[-10:])

## 元组
# 使用()定义的列表无法修改值,可以理解为java的final static
dimensions = (200,50)
print(dimensions[1])
