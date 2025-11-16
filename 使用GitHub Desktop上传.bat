@echo off
chcp 65001 >nul 2>&1
cls
title 使用GitHub Desktop上传（最简单）

echo.
echo ========================================
echo   使用GitHub Desktop上传（最简单）
echo ========================================
echo.
echo [推荐] 如果自动上传失败，使用这个方法
echo.
echo GitHub Desktop的优点:
echo   - 图形界面，更简单
echo   - 自动处理Git操作
echo   - 不需要命令行
echo   - 不需要Token
echo.
echo ========================================
echo.

REM 检查是否已安装
where "GitHub Desktop.exe" >nul 2>&1
if %errorlevel% == 0 (
    echo [检测] GitHub Desktop已安装
    echo [打开] 正在启动GitHub Desktop...
    start "" "GitHub Desktop.exe"
    echo.
    echo [提示] 在GitHub Desktop中:
    echo   1. 登录GitHub账号
    echo   2. File → Add Local Repository
    echo   3. 选择项目目录
    echo   4. Publish repository
    echo.
) else (
    echo [提示] GitHub Desktop未安装
    echo.
    echo [下载] 正在打开下载页面...
    start "" "https://desktop.github.com"
    echo.
    echo [步骤]
    echo   1. 下载并安装GitHub Desktop
    echo   2. 登录GitHub账号
    echo   3. File → Add Local Repository
    echo   4. 选择: C:\Users\Lenovo\Desktop\999999999
    echo   5. Publish repository
    echo   6. 输入仓库名: ssh-tool-android
    echo   7. 选择 Public
    echo   8. 点击 Publish
    echo.
    echo 详细说明: 手动上传到GitHub_最简单.md
    echo.
)

pause

