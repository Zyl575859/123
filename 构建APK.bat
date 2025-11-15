@echo off
chcp 65001 >nul 2>&1
cls
title 使用Python脚本构建APK

echo.
echo ========================================
echo   使用Python脚本构建APK
echo ========================================
echo.

REM 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    where python3 >nul 2>&1
    if %errorlevel% neq 0 (
        echo [错误] 未找到Python
        echo.
        echo 请先安装Python:
        echo   下载: https://www.python.org/downloads/
        echo   安装时勾选 "Add Python to PATH"
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

echo [OK] Python已安装
echo.

REM 检查脚本文件
if not exist "build_apk.py" (
    echo [错误] 未找到 build_apk.py
    echo 请确保在项目根目录运行
    pause
    exit /b 1
)

echo [运行] 启动构建脚本...
echo.

%PYTHON_CMD% build_apk.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 脚本执行失败
    pause
    exit /b 1
)

exit /b 0
