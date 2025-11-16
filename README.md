# What-is-Studied

文件分类系统 / File Classification System

一个智能的文件上传和分类系统，能够根据文件内容自动分类。

An intelligent file upload and classification system that automatically categorizes files based on their content.

## 功能特点 / Features

- 🗂️ **自动分类**: 根据文件类型和内容自动分类
- 📁 **多种类别**: 支持文档、图片、视频、音频、代码、数据、压缩包等
- 🔍 **重复检测**: 自动检测并防止重复文件上传
- 📊 **统计信息**: 查看文件分类统计信息
- 🛠️ **命令行界面**: 简单易用的CLI工具

## 支持的文件类别 / Supported Categories

- **Documents** (文档): PDF, Word, Excel, PowerPoint, Text files
- **Images** (图片): JPEG, PNG, GIF, BMP, SVG, WebP
- **Videos** (视频): MP4, AVI, MOV, WMV, MKV, WebM
- **Audio** (音频): MP3, WAV, OGG, FLAC, AAC
- **Archives** (压缩包): ZIP, RAR, TAR, GZ, 7Z
- **Code** (代码): Python, Java, JavaScript, HTML, CSS, JSON
- **Data** (数据): CSV, JSON, XML, SQL, Database files

## 安装 / Installation

此项目使用Python标准库，无需安装额外依赖。

This project uses Python standard library only, no additional dependencies required.

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/sunisgoing/What-is-Studied.git
cd What-is-Studied

# 确保Python 3.7+ / Ensure Python 3.7+
python --version
```

## 使用方法 / Usage

### 上传文件 / Upload Files

```bash
# 上传单个文件 / Upload a single file
python cli.py upload document.pdf

# 上传多个文件 / Upload multiple files
python cli.py upload image1.jpg image2.png video.mp4

# 使用哈希命名存储 / Store with hash-based names
python cli.py upload --hash-names file.txt
```

### 查看文件列表 / List Files

```bash
# 查看所有文件 / List all files
python cli.py list

# 按类别查看 / List by category
python cli.py list --category images
python cli.py list --category documents
```

### 查看统计信息 / View Statistics

```bash
# 显示分类统计 / Show statistics
python cli.py stats
```

### 查看支持的类别 / View Supported Categories

```bash
# 显示所有支持的文件类别 / Show all supported categories
python cli.py categories
```

## Python API 使用 / Python API Usage

```python
from file_classifier import FileClassifier

# 创建分类器实例 / Create classifier instance
classifier = FileClassifier(upload_dir='uploads')

# 上传文件 / Upload a file
result = classifier.upload_file('path/to/file.pdf')
print(f"Category: {result['file_info']['category']}")

# 列出文件 / List files
files = classifier.list_files(category='images')
for file in files:
    print(f"{file['original_name']} - {file['category']}")

# 获取统计信息 / Get statistics
stats = classifier.get_statistics()
print(f"Total files: {stats['total_files']}")
```

## 运行测试 / Run Tests

```bash
# 运行所有测试 / Run all tests
python -m unittest test_file_classifier.py

# 运行详细测试 / Run tests with verbose output
python -m unittest test_file_classifier.py -v
```

## 项目结构 / Project Structure

```
What-is-Studied/
├── file_classifier.py      # 核心分类逻辑 / Core classification logic
├── cli.py                  # 命令行界面 / CLI interface
├── test_file_classifier.py # 单元测试 / Unit tests
├── requirements.txt        # 依赖项 / Dependencies
├── README.md              # 说明文档 / Documentation
└── uploads/               # 上传文件存储目录 / Upload storage directory
    ├── documents/         # 文档类 / Documents
    ├── images/           # 图片类 / Images
    ├── videos/           # 视频类 / Videos
    ├── audio/            # 音频类 / Audio
    ├── archives/         # 压缩包类 / Archives
    ├── code/             # 代码类 / Code
    ├── data/             # 数据类 / Data
    ├── other/            # 其他类 / Other
    └── metadata.json     # 元数据 / Metadata
```

## 技术特性 / Technical Features

- **SHA256哈希**: 用于重复检测和文件完整性验证
- **MIME类型检测**: 基于文件内容的智能分类
- **扩展名识别**: 支持多种文件扩展名
- **元数据存储**: JSON格式存储文件信息
- **文件名冲突处理**: 自动处理重名文件

## 许可证 / License

MIT License

## 贡献 / Contributing

欢迎提交问题和拉取请求！

Issues and pull requests are welcome!