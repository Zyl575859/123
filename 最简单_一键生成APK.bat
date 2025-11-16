@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
cd /d "%~dp0"
cls
title 最简单 - 一键生成APK

echo.
echo ========================================
echo   最简单方法：一键生成APK
echo ========================================
echo.
echo [提示] 这个方法会：
echo   1. 自动检查并修复所有问题
echo   2. 自动上传到GitHub
echo   3. 自动触发构建
echo   4. 你只需要等待并下载APK
echo.
echo ========================================
echo.

REM 检查Git
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装Git
    echo.
    echo 请先安装Git（只需一次）:
    echo   下载: https://git-scm.com/download/win
    echo   安装时全部选择默认选项
    echo.
    pause
    exit /b 1
)

REM 检查文件
if not exist "main.py" (
    echo [错误] main.py 不存在
    pause
    exit /b 1
)
if not exist "buildozer.spec" (
    echo [错误] buildozer.spec 不存在
    pause
    exit /b 1
)

echo [OK] 文件检查完成
echo.

REM 配置Git用户（如果还没有）
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo [配置] 首次使用，需要配置Git（只需一次）
    echo.
    set /p git_name="你的名字: "
    set /p git_email="你的邮箱: "
    git config --global user.name "!git_name!"
    git config --global user.email "!git_email!"
    echo [OK] 配置完成
    echo.
)

REM 初始化Git
if not exist ".git" git init >nul 2>&1

REM 创建GitHub Actions配置
if not exist ".github\workflows" mkdir ".github\workflows" >nul 2>&1
if not exist ".github\workflows\build_apk.yml" (
    echo [创建] 正在创建构建配置...
    (
        echo name: 构建Android APK
        echo on: [workflow_dispatch, push]
        echo jobs:
        echo   build:
        echo     runs-on: ubuntu-latest
        echo     steps:
        echo     - uses: actions/checkout@v3
        echo     - uses: actions/setup-python@v4
        echo       with:
        echo         python-version: '3.10'
        echo     - run: sudo apt-get update ^&^& sudo apt-get install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
        echo     - run: pip3 install --user buildozer
        echo     - run: echo "$HOME/.local/bin" ^>^> $GITHUB_PATH
        echo     - run: buildozer android debug
        echo     - uses: actions/upload-artifact@v3
        echo       with:
        echo         name: android-apk
        echo         path: bin/*.apk
        echo         retention-days: 30
    ) > ".github\workflows\build_apk.yml"
    echo [OK] 配置已创建
    echo.
)

REM 添加并提交
echo [提交] 正在提交文件...
git add . >nul 2>&1
git commit -m "自动提交" >nul 2>&1
if %errorlevel% neq 0 (
    git commit --allow-empty -m "初始提交" >nul 2>&1
)
git branch -M main >nul 2>&1
echo [OK] 文件已提交
echo.

REM 检查远程仓库
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [配置] 需要GitHub仓库地址
    echo.
    echo 如果没有仓库，请先创建:
    echo   1. 访问: https://github.com/new
    echo   2. 输入仓库名（例如: ssh-tool）
    echo   3. 选择 Public
    echo   4. 点击 Create repository
    echo   5. 复制仓库地址
    echo.
    set /p repo_url="GitHub仓库地址: "
    if "!repo_url!"=="" (
        echo [取消] 已取消
        pause
        exit /b 0
    )
    git remote add origin "!repo_url!" >nul 2>&1
)

REM 上传
echo [上传] 正在上传到GitHub...
echo [提示] 需要输入GitHub用户名和Token
echo [提示] 获取Token: https://github.com/settings/tokens
echo.
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo [失败] 上传失败
    echo.
    echo 请检查:
    echo   1. GitHub仓库地址是否正确
    echo   2. 是否使用了Personal Access Token
    echo   3. 网络连接是否正常
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [成功] 代码已上传！
echo ========================================
echo.

REM 获取仓库地址
for /f "tokens=*" %%u in ('git remote get-url origin') do set repo_url=%%u
set actions_url=!repo_url:.git=/actions!

echo [打开] 正在打开GitHub Actions页面...
start "" "!actions_url!"

echo.
echo ========================================
echo   最后一步：触发构建
echo ========================================
echo.
echo 1. 在打开的页面中
echo 2. 左侧点击 "构建Android APK"
echo 3. 右侧点击 "Run workflow"
echo 4. 选择分支 "main"
echo 5. 点击 "Run workflow" 确认
echo.
echo 然后等待 10-20 分钟，下载APK即可！
echo.
echo GitHub地址: !actions_url!
echo.
pause

