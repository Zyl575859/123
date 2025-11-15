@echo off
chcp 65001 >nul 2>&1
cls
title 最简单构建APK方法

echo.
echo ========================================
echo   最简单构建APK方法
echo ========================================
echo.

echo 请选择构建方法:
echo.
echo [1] 在线构建（推荐，不需要本地环境）
echo [2] 使用Briefcase（本地构建，比Buildozer简单）
echo [3] 查看说明文档
echo.
set /p choice="请选择 (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo [选择] 在线构建
    echo.
    python 在线构建APK.py
) else if "%choice%"=="2" (
    echo.
    echo [选择] Briefcase构建
    echo.
    python build_apk_simple.py
) else if "%choice%"=="3" (
    echo.
    echo 打开说明文档...
    if exist "最简单构建方法.md" (
        notepad "最简单构建方法.md"
    ) else (
        echo 说明文档不存在
    )
) else (
    echo [错误] 无效选择
)

pause

