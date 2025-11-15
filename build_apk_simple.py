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
    
    # 创建简化的配置
    config = """[tool.briefcase]
project_name = "SSH工具"
bundle = "org.liulang"
version = "1.0.0"
url = "https://github.com/liulang/ssh-tool"

[tool.briefcase.app.ssh_tool]
formal_name = "SSH工具"
source = "main.py"

[tool.briefcase.app.ssh_tool.android]
requires = [
    "paramiko>=2.9.0",
]
"""
    
    try:
        with open('pyproject.toml', 'w', encoding='utf-8') as f:
            f.write(config)
        print("[OK] 配置文件已创建")
        return True
    except Exception as e:
        print(f"[失败] 创建配置失败: {e}")
        return False

def build_apk():
    """构建APK"""
    print("\n[构建] 开始构建APK...")
    print("[提示] 首次构建需要下载Android SDK，可能需要较长时间")
    print()
    
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
        print("\nAPK文件位置: android/app/build/outputs/apk/")
        print("\n下一步:")
        print("  1. 找到生成的APK文件")
        print("  2. 复制到Android手机")
        print("  3. 安装并运行")
    else:
        print("\n" + "="*60)
        print("[失败] APK构建失败")
        print("="*60)
        print("\n请查看上方错误信息")
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

