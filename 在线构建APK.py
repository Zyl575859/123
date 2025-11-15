#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在线构建APK - 使用GitHub Actions
完全不需要本地环境，只需要上传代码
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

def check_git():
    """检查Git是否安装"""
    return shutil.which('git') is not None

def init_git():
    """初始化Git仓库"""
    if os.path.exists('.git'):
        return True
    
    print("[初始化] 正在初始化Git仓库...")
    result = subprocess.run(['git', 'init'], capture_output=True, text=True)
    return result.returncode == 0

def create_github_workflow():
    """创建GitHub Actions工作流"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_file = workflow_dir / 'build_apk.yml'
    
    workflow_content = """name: 构建Android APK

on:
  workflow_dispatch:  # 手动触发
  push:
    branches: [ main, master ]
    paths:
      - 'main.py'
      - 'buildozer.spec'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: 检出代码
      uses: actions/checkout@v3
      
    - name: 设置Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: 安装系统依赖
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
        
    - name: 安装Buildozer
      run: |
        pip3 install --user buildozer
        echo "$HOME/.local/bin" >> $GITHUB_PATH
        
    - name: 构建APK
      run: |
        buildozer android debug
        
    - name: 上传APK
      uses: actions/upload-artifact@v3
      with:
        name: android-apk
        path: bin/*.apk
        retention-days: 30
"""
    
    try:
        with open(workflow_file, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        print(f"[OK] GitHub Actions工作流已创建: {workflow_file}")
        return True
    except Exception as e:
        print(f"[失败] 创建工作流失败: {e}")
        return False

def setup_git_user():
    """配置Git用户信息"""
    result = subprocess.run(
        ['git', 'config', 'user.name'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("\n[配置] 需要配置Git用户信息（只需一次）")
        name = input("请输入你的名字: ").strip()
        email = input("请输入你的邮箱: ").strip()
        
        if name and email:
            subprocess.run(['git', 'config', '--global', 'user.name', name])
            subprocess.run(['git', 'config', '--global', 'user.email', email])
            print("[OK] Git用户信息已配置")

def commit_and_push():
    """提交并推送代码"""
    print("\n[提交] 正在提交代码...")
    
    # 添加文件
    subprocess.run(['git', 'add', '.'])
    
    # 提交
    result = subprocess.run(
        ['git', 'commit', '-m', '添加GitHub Actions构建配置'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0 and 'nothing to commit' not in result.stdout:
        print("[失败] 提交失败")
        return False
    
    print("[OK] 代码已提交")
    
    # 检查远程仓库
    result = subprocess.run(
        ['git', 'remote', 'get-url', 'origin'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("\n[配置] 需要添加GitHub远程仓库")
        repo_url = input("请输入GitHub仓库地址（例如: https://github.com/用户名/仓库名.git）: ").strip()
        
        if repo_url:
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
            print("[OK] 远程仓库已配置")
        else:
            print("[提示] 未输入仓库地址，稍后可以手动添加")
            print("命令: git remote add origin <仓库地址>")
            return False
    
    # 推送
    print("\n[推送] 正在推送到GitHub...")
    print("[提示] 如果是第一次，需要输入GitHub用户名和Token")
    
    result = subprocess.run(
        ['git', 'push', '-u', 'origin', 'main'],
        capture_output=False
    )
    
    if result.returncode == 0:
        print("\n[成功] 代码已推送到GitHub！")
        return True
    else:
        print("\n[提示] 推送失败，可能需要:")
        print("  1. 在GitHub上创建仓库")
        print("  2. 使用Personal Access Token认证")
        return False

def main():
    """主函数"""
    print("="*60)
    print("  SSH工具 - 在线构建APK（GitHub Actions）")
    print("="*60)
    print("\n这个方法完全不需要本地构建环境！")
    print("只需要上传代码到GitHub，云端自动构建")
    print()
    
    # 检查Git
    if not check_git():
        print("[错误] 未安装Git")
        print("下载: https://git-scm.com/download/win")
        input("\n按回车键退出...")
        return
    
    # 初始化Git
    if not init_git():
        print("[失败] Git初始化失败")
        input("\n按回车键退出...")
        return
    
    # 创建GitHub Actions工作流
    if not create_github_workflow():
        print("[失败] 创建工作流失败")
        input("\n按回车键退出...")
        return
    
    # 配置Git用户
    setup_git_user()
    
    # 提交并推送
    if commit_and_push():
        print("\n" + "="*60)
        print("[成功] 设置完成！")
        print("="*60)
        print("\n下一步:")
        print("  1. 访问你的GitHub仓库")
        print("  2. 点击 'Actions' 标签")
        print("  3. 选择 '构建Android APK' 工作流")
        print("  4. 点击 'Run workflow' 手动触发构建")
        print("  5. 等待构建完成（约10-20分钟）")
        print("  6. 在Artifacts中下载APK")
    else:
        print("\n" + "="*60)
        print("[提示] 部分步骤未完成")
        print("="*60)
        print("\n你可以:")
        print("  1. 手动在GitHub上创建仓库")
        print("  2. 运行: git remote add origin <仓库地址>")
        print("  3. 运行: git push -u origin main")
        print("  4. 在GitHub Actions中触发构建")
    
    input("\n按回车键退出...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[取消] 已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n[错误] 发生异常: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")

