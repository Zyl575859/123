# 🚀 使用Python脚本构建APK

## 📋 使用方法

### 方法1：直接运行（推荐）

1. **确保已安装Python 3.7+**
   ```bash
   python --version
   ```

2. **运行构建脚本**
   ```bash
   python build_apk.py
   ```

3. **按提示操作**
   - 脚本会自动检测Docker或WSL
   - 选择构建方式
   - 等待构建完成

---

## 🎯 脚本功能

### 自动检测环境
- ✅ 自动检测Docker是否安装和运行
- ✅ 自动检测WSL是否可用
- ✅ 自动选择最佳构建方式

### 自动处理
- ✅ 自动下载Docker镜像（首次）
- ✅ 自动安装Buildozer（WSL方式，首次）
- ✅ 自动检查必要文件
- ✅ 自动查找生成的APK

### 清晰提示
- ✅ 显示构建进度
- ✅ 显示APK文件位置和大小
- ✅ 提供下一步操作指引

---

## 📋 前置要求

### 使用Docker方式（推荐）
1. 安装Docker Desktop
   - 下载：https://www.docker.com/products/docker-desktop
   - 安装并启动Docker Desktop

### 使用WSL方式
1. 安装WSL
   - 在PowerShell（管理员）运行：`wsl --install`
   - 重启电脑

---

## 🔧 脚本参数

目前脚本支持交互式操作，后续可以添加命令行参数：

```bash
# 强制使用Docker
python build_apk.py --docker

# 强制使用WSL
python build_apk.py --wsl

# 静默模式（不显示交互提示）
python build_apk.py --quiet
```

---

## ❓ 常见问题

### Q: 提示"缺少必要文件"？
A: 确保在项目根目录运行脚本，且存在 `main.py` 和 `buildozer.spec`

### Q: Docker未运行？
A: 手动启动Docker Desktop，等待完全启动后再运行脚本

### Q: 构建失败？
A: 查看错误信息，通常是：
- 网络问题（需要下载依赖）
- 磁盘空间不足（至少需要5GB）
- Docker/WSL配置问题

### Q: 找不到APK文件？
A: 检查 `bin/` 目录，如果不存在说明构建失败

---

## 💡 提示

- **首次构建**需要下载大量文件，请保持网络稳定
- **构建时间**：首次30分钟-1小时，后续5-10分钟
- **APK位置**：构建成功后会在 `bin/` 目录

---

## 🎉 开始构建

现在就运行：
```bash
python build_apk.py
```

然后按照提示操作即可！


