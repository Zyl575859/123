#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超简单APK构建脚本
使用BeeWare Briefcase（比Buildozer更简单）
"""

import os
import sys
import subprocess
import shutil

def check_python():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("[错误] 需要Python 3.7或更高版本")
        return False
    print(f"[OK] Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def install_briefcase():
    """安装Briefcase"""
    print("\n[安装] 正在安装BeeWare Briefcase...")
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '--upgrade', 'briefcase'],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("[OK] Briefcase安装完成")
        return True
    else:
        print("[失败] Briefcase安装失败")
        print(result.stderr)
        return False

def check_briefcase():
    """检查Briefcase是否安装"""
    result = subprocess.run(
        [sys.executable, '-m', 'briefcase', '--version'],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def init_briefcase():
    """初始化Briefcase项目"""
    print("\n[初始化] 正在初始化Briefcase项目...")
    
    # 检查是否已初始化
    if os.path.exists('pyproject.toml'):
        print("[提示] 项目已初始化，跳过")
        return True
    
    result = subprocess.run(
        [sys.executable, '-m', 'briefcase', 'new'],
        input='SSH工具\norg.liulang\nSSH工具\n1.0.0\n',
        text=True,
        capture_output=True
    )
    
    if result.returncode == 0:
        print("[OK] 项目初始化完成")
        return True
    else:
        print("[失败] 项目初始化失败")
        # 手动创建配置
        return create_manual_config()

def create_manual_config():
    """手动创建Briefcase配置"""
    print("[提示] 尝试手动创建配置...")
    
    # 检查是否已存在配置文件
    if os.path.exists('pyproject.toml'):
        print("[提示] 配置文件已存在，检查是否需要更新...")
        try:
            with open('pyproject.toml', 'r', encoding='utf-8') as f:
                content = f.read()
            if 'description' in content and 'license' in content:
                print("[OK] 配置文件完整")
                return True
        except:
            pass
    
    # 创建完整的配置
    config = """[tool.briefcase]
project_name = "SSH工具"
bundle = "org.liulang"
version = "1.0.1"
url = "https://github.com/liulang/ssh-tool"
license = "MIT"
description = "SSH连接工具Android版本"

[tool.briefcase.app.ssh_tool]
formal_name = "SSH工具"
description = "SSH连接工具，支持服务器管理和命令执行"
source = "main.py"
license = "MIT"

[tool.briefcase.app.ssh_tool.android]
requires = [
    "paramiko>=2.9.0",
]
permissions = [
    "INTERNET",
    "ACCESS_NETWORK_STATE",
]
"""
    
    try:
        with open('pyproject.toml', 'w', encoding='utf-8') as f:
            f.write(config)
        print("[OK] 配置文件已创建/更新")
        return True
    except Exception as e:
        print(f"[失败] 创建配置失败: {e}")
        return False

def build_apk():
    """构建APK"""
    print("\n[构建] 开始构建APK...")
    print("[提示] 首次构建需要下载Android SDK，可能需要较长时间")
    print("[提示] 这可能需要30分钟-1小时，请耐心等待...")
    print()
    
    # 先更新项目（确保配置正确）
    print("[更新] 更新Briefcase项目配置...")
    update_result = subprocess.run(
        [sys.executable, '-m', 'briefcase', 'update', 'android'],
        capture_output=True,
        text=True
    )
    
    if update_result.returncode != 0:
        print("[警告] 更新配置时出现警告，继续构建...")
        print(update_result.stderr)
    
    print("\n[构建] 开始构建APK...")
    result = subprocess.run(
        [sys.executable, '-m', 'briefcase', 'build', 'android'],
        capture_output=False
    )
    
    return result.returncode == 0

def main():
    """主函数"""
    print("="*60)
    print("  SSH工具 - 超简单APK构建（使用Briefcase）")
    print("="*60)
    
    # 检查Python
    if not check_python():
        input("\n按回车键退出...")
        return
    
    # 检查Briefcase
    if not check_briefcase():
        print("\n[提示] Briefcase未安装")
        choice = input("是否安装Briefcase? (Y/n): ").strip().lower()
        if choice != 'n':
            if not install_briefcase():
                input("\n按回车键退出...")
                return
        else:
            print("[取消] 已取消")
            input("\n按回车键退出...")
            return
    
    # 初始化项目
    if not init_briefcase():
        print("\n[失败] 初始化失败")
        input("\n按回车键退出...")
        return
    
    # 构建APK
    if build_apk():
        print("\n" + "="*60)
        print("[成功] APK构建完成！")
        print("="*60)
        
        # 查找APK文件
        apk_paths = [
            'android/app/build/outputs/apk/debug/app-debug.apk',
            'android/app/build/outputs/apk/release/app-release.apk',
            'android/app/build/outputs/apk/',
        ]
        
        apk_found = False
        for path in apk_paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    print(f"\nAPK文件位置: {os.path.abspath(path)}")
                    size = os.path.getsize(path) / 1024 / 1024
                    print(f"文件大小: {size:.2f} MB")
                    apk_found = True
                    break
                elif os.path.isdir(path):
                    # 查找目录中的APK文件
                    import glob
                    apks = glob.glob(os.path.join(path, '**/*.apk'), recursive=True)
                    if apks:
                        apk_file = apks[0]
                        print(f"\nAPK文件位置: {os.path.abspath(apk_file)}")
                        size = os.path.getsize(apk_file) / 1024 / 1024
                        print(f"文件大小: {size:.2f} MB")
                        apk_found = True
                        break
        
        if not apk_found:
            print("\nAPK文件位置: android/app/build/outputs/apk/")
            print("（请在该目录中查找APK文件）")
        
        print("\n下一步:")
        print("  1. 找到生成的APK文件")
        print("  2. 复制到Android手机")
        print("  3. 在手机上启用'未知来源'安装")
        print("  4. 点击APK文件安装")
    else:
        print("\n" + "="*60)
        print("[失败] APK构建失败")
        print("="*60)
        print("\n请查看上方错误信息")
        print("\n常见问题:")
        print("  1. 配置不完整 - 已自动修复，请重新运行")
        print("  2. Android SDK下载失败 - 检查网络连接")
        print("  3. 依赖安装失败 - 检查Python环境")
        print("\n提示: Briefcase需要Android SDK，首次使用会自动下载")
    
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

