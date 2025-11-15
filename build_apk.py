#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动构建Android APK脚本
支持Docker和WSL两种方式
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"[步骤{step}] {message}")
    print('='*60)

def check_command(cmd):
    """检查命令是否存在"""
    return shutil.which(cmd) is not None

def run_command(cmd, shell=False, check=True):
    """运行命令"""
    try:
        if isinstance(cmd, str):
            cmd = cmd.split()
        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def check_docker():
    """检查Docker是否可用"""
    if not check_command('docker'):
        return False, "Docker未安装"
    
    # 检查Docker是否运行
    result = subprocess.run(
        ['docker', 'ps'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Docker未运行，请先启动Docker Desktop"
    
    return True, "Docker可用"

def check_wsl():
    """检查WSL是否可用"""
    if not check_command('wsl'):
        return False, "WSL未安装"
    
    # 检查WSL是否可用
    result = subprocess.run(
        ['wsl', '--list'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "WSL不可用"
    
    return True, "WSL可用"

def build_with_docker():
    """使用Docker构建"""
    print_step(1, "检查Docker镜像")
    
    # 检查镜像是否存在
    result = subprocess.run(
        ['docker', 'images', 'kivy/buildozer', '--format', '{{.Repository}}:{{.Tag}}'],
        capture_output=True,
        text=True
    )
    
    if 'kivy/buildozer' not in result.stdout:
        print("[提示] 首次使用，需要下载Docker镜像（约500MB）")
        print("[提示] 这可能需要几分钟，请耐心等待...")
        if not run_command(['docker', 'pull', 'kivy/buildozer']):
            return False
        print("[OK] 镜像下载完成")
    else:
        print("[OK] 镜像已存在")
    
    print_step(2, "开始构建APK")
    print("[提示] 首次构建需要30分钟-1小时，请耐心等待...")
    print("[提示] 构建过程中请不要关闭此窗口")
    print()
    
    # 获取当前目录
    current_dir = os.getcwd()
    
    # 构建命令
    cmd = [
        'docker', 'run', '--rm',
        '--volume', f'{current_dir}:/home/user/hostcwd',
        'kivy/buildozer',
        'buildozer', 'android', 'debug'
    ]
    
    return run_command(cmd, check=False)

def build_with_wsl():
    """使用WSL构建"""
    print_step(1, "检查WSL环境")
    
    # 检查buildozer是否安装
    result = subprocess.run(
        ['wsl', 'bash', '-c', 'command -v buildozer'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("[提示] 首次使用，需要安装Buildozer")
        print("[提示] 这可能需要几分钟，请耐心等待...")
        
        install_cmd = [
            'wsl', 'bash', '-c',
            'sudo apt-get update -qq && '
            'sudo apt-get install -y -qq git zip unzip openjdk-11-jdk python3-pip '
            'autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev '
            'libtinfo5 cmake libffi-dev libssl-dev > /dev/null 2>&1 && '
            'pip3 install --user buildozer > /dev/null 2>&1'
        ]
        
        if not run_command(install_cmd, check=False):
            print("[失败] Buildozer安装失败")
            return False
        
        print("[OK] Buildozer安装完成")
    else:
        print("[OK] Buildozer已安装")
    
    print_step(2, "开始构建APK")
    print("[提示] 首次构建需要30分钟-1小时，请耐心等待...")
    print()
    
    # 获取Windows路径对应的WSL路径
    current_dir = os.getcwd()
    # 转换Windows路径到WSL路径
    wsl_path = current_dir.replace('C:\\', '/mnt/c/').replace('\\', '/')
    
    # 构建命令
    build_cmd = f'cd {wsl_path} && export PATH=$PATH:~/.local/bin && buildozer android debug'
    cmd = ['wsl', 'bash', '-c', build_cmd]
    
    return run_command(cmd, check=False)

def check_files():
    """检查必要文件是否存在"""
    required_files = ['main.py', 'buildozer.spec']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"[错误] 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    return True

def find_apk():
    """查找生成的APK文件"""
    bin_dir = Path('bin')
    if not bin_dir.exists():
        return None
    
    apk_files = list(bin_dir.glob('*.apk'))
    if apk_files:
        return apk_files[0]
    return None

def main():
    """主函数"""
    print("="*60)
    print("  SSH工具 - Android APK 自动构建")
    print("="*60)
    
    # 检查必要文件
    if not check_files():
        print("\n请确保在项目根目录运行此脚本")
        input("\n按回车键退出...")
        return
    
    # 检查构建环境
    print("\n[检查] 正在检查构建环境...")
    
    docker_ok, docker_msg = check_docker()
    wsl_ok, wsl_msg = check_wsl()
    
    if docker_ok:
        print(f"[OK] {docker_msg}")
        print("\n[推荐] 使用Docker构建（更简单）")
        choice = input("使用Docker构建? (Y/n): ").strip().lower()
        if choice != 'n':
            success = build_with_docker()
        elif wsl_ok:
            print(f"\n[切换] {wsl_msg}")
            success = build_with_wsl()
        else:
            print(f"\n[错误] {wsl_msg}")
            success = False
    elif wsl_ok:
        print(f"[OK] {wsl_msg}")
        print("\n[使用] WSL构建")
        success = build_with_wsl()
    else:
        print(f"[错误] {docker_msg}")
        print(f"[错误] {wsl_msg}")
        print("\n请安装以下工具之一：")
        print("  1. Docker Desktop: https://www.docker.com/products/docker-desktop")
        print("  2. WSL: 在PowerShell（管理员）运行: wsl --install")
        input("\n按回车键退出...")
        return
    
    # 检查构建结果
    print("\n" + "="*60)
    if success:
        apk_file = find_apk()
        if apk_file:
            print("[成功] 构建完成！")
            print(f"\nAPK文件位置: {apk_file}")
            print(f"文件大小: {apk_file.stat().st_size / 1024 / 1024:.2f} MB")
            print("\n下一步:")
            print("  1. 将APK文件复制到Android手机")
            print("  2. 在手机上启用'未知来源'安装")
            print("  3. 点击APK文件安装")
        else:
            print("[警告] 构建完成，但未找到APK文件")
            print("请检查构建日志")
    else:
        print("[失败] 构建失败")
        print("\n请查看上方错误信息")
        print("常见问题:")
        print("  1. Docker Desktop未启动")
        print("  2. 网络连接问题")
        print("  3. 磁盘空间不足")
    
    print("="*60)
    input("\n按回车键退出...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[取消] 构建已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n[错误] 发生异常: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")

