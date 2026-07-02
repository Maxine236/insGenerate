本项目 fork 自 kakaoxy/insGenerate，修复了以下问题：

原脚本不读取 -i 参数指定的链接文件（文件名被写死为 11-25.txt）
不识别 instagram.com/用户名/reel/xxx 新版链接格式
依赖清单与 Python 3.14 不兼容，实际只需安装：yt-dlp、fake-useragent、browser-cookie3

# Instagram 视频批量下载与合并工具

这是一个用于批量下载Instagram视频并将其合并的工具套件，包含三个主要组件：视频下载器、视频合并器和Web界面。

## 功能特点

- 批量下载Instagram视频
- 自动生成过渡画面
- 视频合并与转场效果
- 支持自定义标题和作者
- 支持多种颜色方案
- 美观的进度显示
- 直观的Web操作界面
- 支持视频预览和手动排序

## 快速开始

### 安装

1. 克隆项目：
```bash
git clone https://github.com/kakaoxy/insGenerate.git
cd insGenerate
```

2. 安装依赖：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. 创建cookies文件：
登录Instagram，使用cookie editor或其他浏览器工具导出Netscape格式的cookies，并将cookies.txt保存到项目文件夹中。

4. 设置启动脚本权限（仅macOS/Linux）：
```bash
chmod +x start.command
```

### 基本使用

#### 方式一：图形界面启动（推荐）

1. macOS用户：
   - 双击 `start.command` 文件启动程序
   - 如果遇到"无法打开"的安全提示：
     * 打开系统偏好设置
     * 点击"安全性与隐私"
     * 在"通用"标签中点击"仍要打开"

2. Windows/Linux用户：
   - 双击 `start.sh` 文件启动程序
   - 或在终端中执行：
   ```bash
   ./start.sh
   ```

3. 在浏览器中使用：
   - 程序启动后会自动打开浏览器窗口（http://127.0.0.1:8080）
   - 如果浏览器没有自动打开，请手动访问上述地址

4. Web界面使用：
   - 在"下载视频"标签页：
     * 粘贴Instagram视频链接
     * 选择输出目录
     * 点击"开始下载"
   - 在"合并视频"标签页：
     * 选择要合并的视频
     * 预览视频内容
     * 设置第一个视频（其他视频将按文件名排序）
     * 设置输出文件名
     * 添加标题和作者信息
     * 选择过渡画面颜色方案
     * 点击"开始合并"

#### 方式二：命令行

1. 准备视频链接文件（links.txt）：
```
https://www.instagram.com/reel/xxx
https://www.instagram.com/reel/yyy
https://www.instagram.com/reel/zzz
```

2. 下载视频：
```bash
python video_downloader.py -i links.txt -o ./11-23
```

3. 合并视频：
```bash
python video_merger.py -i "11-23" -o "11-23-final.mp4" -c "p1"
```

## 详细使用说明

### 1. Web界面 (web_ui.py)

提供图形化界面，方便直观地操作下载和合并功能。

#### 主要功能：
- 视频下载：
  * 支持单个或批量链接输入
  * 实时显示下载进度
  * 自动创建输出目录

- 视频合并：
  * 视频预览功能
  * 支持手动设置第一个视频
  * 其他视频自动按文件名排序
  * 自定义标题和作者信息
  * 自定义过渡画面颜色方案
  * 实时显示合并进度

#### 颜色方案
提供6种精心设计的过渡画面颜色方案：

| 方案代码 | 名称 | 背景色 | 文字色 | 适用场景 |
|---------|------|--------|--------|----------|
| p1 | 经典黑白 | #FFFFFF | #333333 | 正式、商务 |
| p2 | 柔和灰白 | #F5F5F5 | #2C3E50 | 优雅、简约 |
| p3 | 暖色调 | #FFF8F0 | #8B4513 | 温馨、生活 |
| p4 | 冷色调 | #F0F8FF | #1B4F72 | 科技、专业 |
| p5 | 现代灰白 | #333333 | #FFFFFF | 时尚、潮流 |
| p6 | 经典白黑 | #000000 | #FFFFFF | 高端、大气 |

### 2. 下载视频 (video_downloader.py)

提供Instagram视频下载功能。

#### 命令行参数：
- `-i, --input`: 输入文件路径（包含视频链接的文本文件）
- `-o, --output`: 输出目录路径
- `-s, --single`: 单个视频链接

#### 示例：
```bash
# 从文件批量下载
python video_downloader.py -i links.txt -o ./videos

# 下载单个视频
python video_downloader.py -s "https://www.instagram.com/reel/xxx" -o ./videos
```

### 3. 合并视频 (video_merger.py)

提供视频合并功能，支持自定义过渡画面。

#### 命令行参数：
- `-i, --input_dir`: 输入视频目录
- `-o, --output`: 输出视频文件路径
- `-t, --title`: 视频标题（默认："今日份快乐"）
- `-a, --author`: 作者名称（默认："Cynvann"）
- `-c, --color_scheme`: 过渡画面颜色方案（默认："p6"）

#### 示例：
```bash
# 基本使用
python video_merger.py -i "11-23" -o "11-23-final.mp4"

# 自定义标题和作者
python video_merger.py -i "11-23" -o "output.mp4" -t "我的视频" -a "作者名"

# 指定颜色方案
python video_merger.py -i "11-23" -o "output.mp4" -c "p3"
```

## 更新日志

### v1.1.2 (2024-03-20)
- 添加便捷启动脚本
  * 支持 macOS 系统一键启动（start.command）
  * 支持 Windows/Linux 系统启动（start.sh）
  * 自动检测和创建虚拟环境
  * 优化启动体验和错误提示

### v1.1.1
- 优化过渡画面文件管理
  * 自动清理临时过渡画面文件
  * 改进文件清理机制，确保不留残余文件
  * 添加文件清理日志记录
- 修复已知问题
  * 解决过渡画面文件未及时清理的问题
  * 优化临时文件处理逻辑

### v1.1.0
- 添加过渡画面颜色方案功能
- 支持6种预设颜色方案
- 优化Web界面，添加颜色方案选择
- 改进命令行工具，支持颜色方案参数

### v1.0.0
- 初始版本发布
- 支持批量下载Instagram视频
- 实现视频合并功能
- 添加过渡画面效果
