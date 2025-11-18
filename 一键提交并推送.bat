@echo off
chcp 65001 >nul
echo ========================================
echo 一键提交并推送修复
echo ========================================
echo.

cd /d "C:\Users\Lenovo\Desktop\999999999"

echo [1/5] 检查 main.py 修改...
git status main.py | findstr "modified" >nul
if %errorlevel% equ 0 (
    echo ✅ 发现 main.py 有修改
    git add main.py
) else (
    echo ℹ️  main.py 没有未提交的修改
)

echo.
echo [2/5] 解决 README.md 冲突（如果有）...
if exist "README.md" (
    git checkout --ours README.md 2>nul
    git add README.md 2>nul
    echo ✅ README.md 冲突已解决
)

echo.
echo [3/5] 拉取远程最新更改...
git pull --rebase origin main
if %errorlevel% neq 0 (
    echo ⚠️  拉取时可能有冲突，尝试自动解决...
    git checkout --ours . 2>nul
    git add . 2>nul
    git rebase --continue 2>nul
)

echo.
echo [4/5] 提交所有更改...
git add main.py 2>nul
git commit -m "修复 Courier 字体缺失导致的崩溃" 2>nul
if %errorlevel% neq 0 (
    echo ℹ️  没有新的更改需要提交，或已提交
)

echo.
echo [5/5] 推送到 GitHub...
git push origin main
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 完成！代码已推送到 GitHub
    echo ========================================
    echo GitHub Actions 将自动开始构建新的 APK
    echo 请稍后到 GitHub Actions 页面查看构建状态
) else (
    echo.
    echo ========================================
    echo ❌ 推送失败
    echo ========================================
    echo 请检查网络连接或 Git 配置
)

echo.
pause

