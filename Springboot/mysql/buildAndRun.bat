@echo off
echo 请选择执行方式
echo 1:跳过测试类启动服务
echo 2:编译最新代码并运行
echo 3:打包jar
echo 4:打包jar并运行
set /p usercmd=请输入命令：

if "%usercmd%"=="1" (
	echo 跳过测试类启动服务
	start "SERVER" java -jar target/mysql-1.0-SNAPSHOT.jar
	cd D:\Projects\WebProgram\vue3-project
	start "VUE" Run.bat
) else if "%usercmd%"=="2" (
	echo 编译最新代码并运行
    start mvn clean spring-boot:run
	start "VUE" Run.bat
) else if "%usercmd%"=="3" (
	echo 打包jar
    start mvn clean package
) else (
	echo 打包jar并运行
    start mvn clean package -Dmaven.test.skip=true && java -jar target/mysql-1.0-SNAPSHOT.jar
)
