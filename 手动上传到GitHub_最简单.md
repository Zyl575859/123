# 📤 手动上传到GitHub - 最简单方法

## 🎯 如果自动上传失败，用手动方法

### 方法1：使用GitHub网页上传（最简单）⭐

1. **访问GitHub创建仓库**
   - 打开：https://github.com/new
   - 输入仓库名：`ssh-tool-android`
   - 选择 Public
   - 点击 "Create repository"

2. **上传文件**
   - 在仓库页面，点击 "uploading an existing file"
   - 上传这3个文件：
     - `main.py`
     - `buildozer.spec`
     - `.github/workflows/build_apk.yml`（需要先创建目录）

3. **创建GitHub Actions文件**
   - 点击 "Add file" → "Create new file"
   - 路径输入：`.github/workflows/build_apk.yml`
   - 复制以下内容：

```yaml
name: 构建Android APK
on: [workflow_dispatch, push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - run: sudo apt-get update && sudo apt-get install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    - run: pip3 install --user buildozer
    - run: echo "$HOME/.local/bin" >> $GITHUB_PATH
    - run: buildozer android debug
    - uses: actions/upload-artifact@v3
      with:
        name: android-apk
        path: bin/*.apk
        retention-days: 30
```

4. **提交文件**
   - 点击 "Commit new file"
   - 完成！

---

### 方法2：使用GitHub Desktop（推荐）

1. **下载GitHub Desktop**
   - 访问：https://desktop.github.com
   - 下载并安装

2. **登录GitHub账号**
   - 打开GitHub Desktop
   - 登录你的GitHub账号

3. **添加本地仓库**
   - 点击 "File" → "Add Local Repository"
   - 选择项目目录：`C:\Users\Lenovo\Desktop\999999999`
   - 点击 "Add repository"

4. **发布到GitHub**
   - 点击 "Publish repository"
   - 输入仓库名：`ssh-tool-android`
   - 选择 Public
   - 点击 "Publish repository"

完成！比命令行简单多了！

---

## 🎯 上传后操作

1. **进入GitHub仓库**
2. **点击 "Actions" 标签**
3. **点击 "构建Android APK"**
4. **点击 "Run workflow"**
5. **等待构建完成**
6. **下载APK**

---

## 💡 推荐

**如果自动上传失败，使用GitHub Desktop最简单！**

下载：https://desktop.github.com

安装后：
1. 登录GitHub
2. 添加本地仓库
3. 发布到GitHub
4. 完成！

