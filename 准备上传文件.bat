@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
cls
title 准备上传文件到GitHub

echo.
echo ========================================
echo   准备上传文件到GitHub
echo ========================================
echo.

echo [检查] 正在检查必需文件...
echo.

set MISSING=0

REM 检查main.py
if exist "main.py" (
    echo [OK] main.py
) else (
    echo [错误] main.py 不存在
    set MISSING=1
)

REM 检查buildozer.spec
if exist "buildozer.spec" (
    echo [OK] buildozer.spec
) else (
    echo [错误] buildozer.spec 不存在
    set MISSING=1
)

REM 检查GitHub Actions配置
if exist ".github\workflows\build_apk.yml" (
    echo [OK] .github\workflows\build_apk.yml
) else (
    echo [警告] .github\workflows\build_apk.yml 不存在
    echo [提示] 如果使用在线构建，需要此文件
)

echo.
echo ========================================
echo   需要上传的文件清单
echo ========================================
echo.

if %MISSING%==0 (
    echo [必需文件]
    echo   1. main.py
    echo   2. buildozer.spec
    echo.
    if exist ".github\workflows\build_apk.yml" (
        echo   3. .github\workflows\build_apk.yml
        echo.
    )
    echo [可选文件]
    echo   - README.md (推荐)
    echo   - requirements.txt (如果有)
    echo.
    echo ========================================
    echo   文件位置
    echo ========================================
    echo.
    echo 当前目录: %CD%
    echo.
    echo main.py: %CD%\main.py
    echo buildozer.spec: %CD%\buildozer.spec
    if exist ".github\workflows\build_apk.yml" (
        echo GitHub Actions: %CD%\.github\workflows\build_apk.yml
    )
    echo.
    echo ========================================
    echo   上传方法
    echo ========================================
    echo.
    echo [方法1] 使用GitHub网页上传
    echo   1. 访问: https://github.com/new
    echo   2. 创建新仓库
    echo   3. 点击 "uploading an existing file"
    echo   4. 上传上述文件
    echo.
    echo [方法2] 使用Git命令
    echo   git init
    echo   git add main.py buildozer.spec
    if exist ".github\workflows\build_apk.yml" (
        echo   git add .github\workflows\build_apk.yml
    )
    echo   git commit -m "初始提交"
    echo   git remote add origin https://github.com/用户名/仓库名.git
    echo   git push -u origin main
    echo.
) else (
    echo [错误] 缺少必需文件，请先确保文件存在
    echo.
)

echo 详细说明请查看: 需要上传的文件清单.md
echo.
pause


