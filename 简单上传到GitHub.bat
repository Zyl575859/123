@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
cls
title 简单上传到GitHub

echo.
echo ========================================
echo   简单上传到GitHub
echo ========================================
echo.

REM 检查Git
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装Git
    echo 下载: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM 配置用户信息
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo [配置] 请输入Git用户信息
    set /p git_name="你的名字: "
    set /p git_email="你的邮箱: "
    git config --global user.name "!git_name!"
    git config --global user.email "!git_email!"
)

REM 初始化
if not exist ".git" git init

REM 添加并提交
git add .
git commit -m "初始提交" >nul 2>&1
git branch -M main >nul 2>&1

REM 配置远程仓库
echo.
echo [提示] 请先在GitHub创建仓库: https://github.com/new
echo.
set /p repo_url="GitHub仓库地址: "

if "!repo_url!"=="" (
    echo [取消] 未输入地址
    pause
    exit /b 0
)

git remote remove origin >nul 2>&1
git remote add origin "!repo_url!"

REM 上传
echo.
echo [上传] 正在上传...
echo [提示] 需要输入GitHub用户名和Token
echo.
git push -u origin main

if %errorlevel% == 0 (
    echo.
    echo [成功] 上传完成！
    echo 访问: !repo_url!
) else (
    echo.
    echo [失败] 上传失败
    echo.
    echo 常见问题:
    echo 1. 仓库不存在 - 请先在GitHub创建仓库
    echo 2. 需要Token - https://github.com/settings/tokens
    echo 3. 地址错误 - 格式: https://github.com/用户名/仓库名.git
)

pause


