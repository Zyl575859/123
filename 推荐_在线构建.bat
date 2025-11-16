@echo off
chcp 65001 >nul 2>&1
cls
title 推荐：在线构建APK（最简单）

echo.
echo ========================================
echo   推荐：在线构建APK（最简单）
echo ========================================
echo.
echo 检测到您没有Docker和WSL环境
echo.
echo [推荐] 使用在线构建方法：
echo   - 完全不需要本地环境
echo   - 不需要Docker/WSL
echo   - 云端自动构建
echo   - 最简单！
echo.
echo ========================================
echo.

REM 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    where python3 >nul 2>&1
    if %errorlevel% neq 0 (
        echo [错误] 未找到Python
        echo 请先安装Python: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

REM 检查在线构建脚本
if not exist "在线构建APK.py" (
    echo [错误] 未找到 在线构建APK.py
    echo.
    echo 请使用以下方法之一:
    echo   1. 使用Briefcase: python build_apk_simple.py
    echo   2. 手动上传到GitHub使用Actions构建
    pause
    exit /b 1
)

echo [运行] 启动在线构建脚本...
echo.
echo [提示] 这个方法会帮您:
echo   1. 创建GitHub Actions配置
echo   2. 上传代码到GitHub
echo   3. 在云端自动构建APK
echo.
pause

%PYTHON_CMD% 在线构建APK.py

pause


