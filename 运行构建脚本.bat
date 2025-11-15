@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
cls
title 运行APK构建脚本

echo.
echo ========================================
echo   运行APK构建脚本
echo ========================================
echo.
echo 当前目录: %CD%
echo.

REM 检查文件是否存在
if not exist "build_apk_simple.py" (
    echo [错误] 未找到 build_apk_simple.py
    echo.
    echo 请确保在项目根目录运行此脚本
    echo 项目根目录应包含:
    echo   - main.py
    echo   - build_apk_simple.py
    echo   - buildozer.spec
    echo.
    pause
    exit /b 1
)

echo [OK] 找到 build_apk_simple.py
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
echo [运行] 正在启动构建脚本...
echo.

%PYTHON_CMD% build_apk_simple.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 脚本执行失败
    pause
    exit /b 1
)

exit /b 0

