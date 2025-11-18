@echo off
setlocal enabledelayedexpansion

REM ========= 配置 =========
set REPO_DIR=C:\Users\Lenovo\Desktop\999999999
set BRANCH=main

REM ========= 开始 =========
echo.
echo [1] 切换到仓库目录: %REPO_DIR%
if not exist "%REPO_DIR%" (
    echo  !!! 目录不存在，检查 REPO_DIR 设置
    pause
    exit /b 1
)
cd /d "%REPO_DIR%"

echo.
echo [2] 自动保留本地版本，丢弃遠端的 README.md（謹慎）
git checkout --ours README.md >nul 2>&1
if errorlevel 1 (
    echo  無法處理 README.md，請確認文件存在
    pause
    exit /b 1
)

echo.
echo [3] 標記衝突已解決
git add README.md

echo.
echo [4] 提交本次合併
git commit -m "自动解决 README 冲突并提交"
if errorlevel 1 (
    echo  提交失敗，請手動檢查
    pause
    exit /b 1
)

echo.
echo [5] 推送到遠端 %BRANCH%
git push origin %BRANCH%
if errorlevel 1 (
    echo  推送失敗，請手動檢查
    pause
    exit /b 1
)

echo.
echo ✅ 完成，一切衝突已解決並推送
pause

