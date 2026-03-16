# JobStreet Jobs Scraper

**Author**: guofang

高性能并发爬虫，用于抓取 JobStreet 新加坡地区的职位信息。支持自定义搜索关键词。

A high-performance concurrent web scraper for JobStreet Singapore job listings with customizable search keywords.

---

[🇨🇳 中文文档](#中文文档) | [🇬🇧 English Documentation](#english-documentation)

**📚 新手教程**: [中文完整教程](TUTORIAL.md) | [English Tutorial](TUTORIAL_EN.md)

---

# 中文文档

## ✨ 特性

- 🚀 **并发爬取**: 使用 4 个浏览器并行抓取，速度提升 15-18 倍
- 💾 **自动保存**: 每页完成后自动保存，防止数据丢失
- 🔄 **断点续传**: 支持从中断处继续爬取
- 📊 **进度汇报**: 每 100 个职位显示进度
- 🛡️ **会话恢复**: 自动检测并恢复过期的浏览器会话
- 📧 **邮箱提取**: 自动从职位描述中提取邮箱地址
- 🔍 **智能去重**: 自动去除重复职位

## 📦 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 确保已安装 Chrome 浏览器

爬虫会自动下载匹配的 ChromeDriver。

## 🚀 使用方法

### 基本使用

```bash
python jobstreet_scraper.py
```

### 配置选项

在 `jobstreet_scraper.py` 中修改以下参数：

```python
# 搜索关键词 URL（第 145 行）⭐ 重要
url = "https://sg.jobstreet.com/telemarketing-jobs"

# 并发浏览器数量（第 166 行）
NUM_WORKERS = 4  # 可调整为 2-8

# 起始页码（第 176 行）
start_page = 1  # 从第几页开始爬

# 输出文件名（第 170 行）
output_file = 'jobstreet_all_jobs.csv'
```

### 更换搜索关键词 🔍

如果想爬取其他类型的职位（不是 telemarketing），需要修改搜索 URL：

#### 方法 1：直接修改代码中的 URL

编辑 `jobstreet_scraper.py` 第 145 行：

```python
# 原来的（telemarketing）
url = "https://sg.jobstreet.com/telemarketing-jobs"

# 改为其他关键词，例如：
url = "https://sg.jobstreet.com/sales-jobs"           # 销售
url = "https://sg.jobstreet.com/marketing-jobs"       # 市场营销
url = "https://sg.jobstreet.com/customer-service-jobs" # 客服
url = "https://sg.jobstreet.com/data-analyst-jobs"    # 数据分析
```

#### 方法 2：从 JobStreet 网站获取正确的 URL

1. 访问 [JobStreet 新加坡](https://sg.jobstreet.com/)
2. 在搜索框输入你想要的关键词（如 "software engineer"）
3. 点击搜索后，复制浏览器地址栏的 URL
4. 将该 URL 粘贴到代码第 145 行

**示例：**
```python
# 搜索 "software engineer" 后得到的 URL
url = "https://sg.jobstreet.com/software-engineer-jobs"
```

#### ⚠️ 注意事项

更换搜索关键词后，建议：

1. **修改输出文件名**，避免覆盖之前的数据：
   ```python
   output_file = 'jobstreet_sales_jobs.csv'  # 根据关键词命名
   ```

2. **删除旧的 CSV 文件**（如果使用相同文件名）：
   ```bash
   rm jobstreet_all_jobs.csv
   ```

3. **重新运行爬虫**：
   ```bash
   python jobstreet_scraper.py
   ```

## 📊 输出格式

生成的 CSV 文件包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| `company_name` | 公司名称 | PERSOL |
| `job_title` | 职位标题 | Banking Telemarketing Executive |
| `job_description` | 完整职位描述 | Job Responsibilities: Answer customer inquiries... |
| `email` | 邮箱地址 | hr@example.com 或 Not available |
| `job_url` | 职位链接 | https://sg.jobstreet.com/job/12345... |

## ⚙️ 工作原理

1. **主浏览器** 浏览职位列表页面
2. **4 个并发浏览器** 同时抓取职位详情
3. **每页完成后** 自动保存到 CSV
4. **自动跳过** 已抓取的职位（断点续传）
5. **最后去重** 确保数据唯一性

## 📈 性能

- **串行版本**: ~2-3 分钟/页
- **并发版本 (4浏览器)**: ~10 秒/页
- **速度提升**: 约 15-18 倍

示例：抓取 25 页 (~800 个职位)
- 串行: ~60 分钟
- 并发: ~3-4 分钟 ⚡

## 🔧 高级功能

### 断点续传

如果爬虫中断，直接重新运行即可：
```bash
python jobstreet_scraper.py
```
爬虫会自动：
- 读取已保存的数据
- 跳过已有的职位
- 从中断处继续

### 修改起始页

编辑第 127 行：
```python
start_page = 10  # 从第 10 页开始
```

### 清空重新开始

```bash
# 删除旧数据文件
rm jobstreet_all_jobs.csv
# 重新运行
python jobstreet_scraper.py
```

## 📝 注意事项

### 1. 速度控制
- 默认配置已优化，无需调整
- 如遇到封禁，可减少 `NUM_WORKERS` 到 2-3

### 2. 数据质量
- ✅ 100% 成功率提取职位描述
- ✅ 自动处理 Unicode 和特殊字符
- ✅ 智能提取邮箱地址

### 3. 法律合规
- ⚖️ 仅用于个人研究和学习
- ⚖️ 遵守网站 robots.txt 和使用条款
- ⚖️ 不要过度频繁爬取

### 4. Excel 兼容性
输出的 CSV 文件使用 UTF-8 BOM 编码，可直接用 Excel/WPS 打开。

如果看到多余行数，这是正常的（职位描述包含换行符）。实际职位数以数据行数为准。

## 🛠️ 故障排除

### ChromeDriver 错误
```bash
pip install --upgrade webdriver-manager
```

### 找不到元素
网站结构可能更新，检查 CSS 选择器：
- `article[data-automation="normalJob"]` (职位卡片)
- `div[data-automation="jobDescription"]` (职位描述)

### 会话过期
爬虫会自动重试，无需手动干预。

### 内存占用高
4 个浏览器会占用 ~2GB 内存，如果内存不足：
```python
NUM_WORKERS = 2  # 减少为 2 个浏览器
```

## 📂 输出示例

最终会生成：
- `jobstreet_all_jobs.csv` - 原始数据
- `jobstreet_final_merged_fixed.csv` - 去重后的最终数据（推荐使用）

## 🎯 项目目标

抓取 JobStreet 新加坡地区的职位信息。默认配置为电话销售相关职位，可修改为任意关键词：
- 📞 Telemarketing（默认）
- 💼 Sales, Marketing, Customer Service
- 💻 IT, Software Engineering, Data Analysis
- 🏢 或任何其他职位类型

详见上方 [更换搜索关键词](#更换搜索关键词-) 部分。

---

**© 2025 guofang | 仅供教育和研究用途**

---

# English Documentation

## ✨ Features

- 🚀 **Concurrent Scraping**: Uses 4 parallel browsers, 15-18x faster
- 💾 **Auto-Save**: Saves after each page to prevent data loss
- 🔄 **Resume Support**: Continue from where you left off
- 📊 **Progress Reports**: Shows progress every 100 jobs
- 🛡️ **Session Recovery**: Automatically detects and recovers expired browser sessions
- 📧 **Email Extraction**: Extracts email addresses from job descriptions
- 🔍 **Smart Deduplication**: Automatically removes duplicate jobs

## 📦 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Chrome Browser is Installed

The scraper will automatically download the matching ChromeDriver.

## 🚀 Usage

### Basic Usage

```bash
python jobstreet_scraper.py
```

### Configuration Options

Modify the following parameters in `jobstreet_scraper.py`:

```python
# Search keyword URL (Line 145) ⭐ Important
url = "https://sg.jobstreet.com/telemarketing-jobs"

# Number of concurrent browsers (Line 166)
NUM_WORKERS = 4  # Adjustable to 2-8

# Starting page number (Line 176)
start_page = 1  # Which page to start from

# Output filename (Line 170)
output_file = 'jobstreet_all_jobs.csv'
```

### Changing Search Keywords 🔍

To scrape jobs other than telemarketing, modify the search URL:

#### Method 1: Directly Modify URL in Code

Edit line 145 in `jobstreet_scraper.py`:

```python
# Original (telemarketing)
url = "https://sg.jobstreet.com/telemarketing-jobs"

# Change to other keywords, for example:
url = "https://sg.jobstreet.com/sales-jobs"           # Sales
url = "https://sg.jobstreet.com/marketing-jobs"       # Marketing
url = "https://sg.jobstreet.com/customer-service-jobs" # Customer Service
url = "https://sg.jobstreet.com/data-analyst-jobs"    # Data Analysis
```

#### Method 2: Get Correct URL from JobStreet Website

1. Visit [JobStreet Singapore](https://sg.jobstreet.com/)
2. Enter your desired keyword in the search box (e.g., "software engineer")
3. After searching, copy the URL from your browser's address bar
4. Paste that URL to line 145 in the code

**Example:**
```python
# URL obtained after searching "software engineer"
url = "https://sg.jobstreet.com/software-engineer-jobs"
```

#### ⚠️ Important Notes

After changing search keywords, it's recommended to:

1. **Modify the output filename** to avoid overwriting previous data:
   ```python
   output_file = 'jobstreet_sales_jobs.csv'  # Name based on keyword
   ```

2. **Delete old CSV file** (if using the same filename):
   ```bash
   rm jobstreet_all_jobs.csv
   ```

3. **Re-run the scraper**:
   ```bash
   python jobstreet_scraper.py
   ```

## 📊 Output Format

The generated CSV file contains the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| `company_name` | Company name | PERSOL |
| `job_title` | Job title | Banking Telemarketing Executive |
| `job_description` | Full job description | Job Responsibilities: Answer customer inquiries... |
| `email` | Email address | hr@example.com or Not available |
| `job_url` | Job link | https://sg.jobstreet.com/job/12345... |

## ⚙️ How It Works

1. **Main browser** browses job listing pages
2. **4 concurrent browsers** simultaneously scrape job details
3. **Auto-saves after each page** to CSV
4. **Automatically skips** already scraped jobs (resume support)
5. **Final deduplication** ensures data uniqueness

## 📈 Performance

- **Serial version**: ~2-3 minutes/page
- **Concurrent version (4 browsers)**: ~10 seconds/page
- **Speed improvement**: Approximately 15-18x

Example: Scraping 25 pages (~800 jobs)
- Serial: ~60 minutes
- Concurrent: ~3-4 minutes ⚡

## 🔧 Advanced Features

### Resume Support

If the scraper is interrupted, simply re-run:
```bash
python jobstreet_scraper.py
```
The scraper will automatically:
- Read saved data
- Skip existing jobs
- Continue from where it left off

### Modify Starting Page

Edit line 176:
```python
start_page = 10  # Start from page 10
```

### Clear and Start Fresh

```bash
# Delete old data file
rm jobstreet_all_jobs.csv
# Re-run
python jobstreet_scraper.py
```

## 📝 Notes

### 1. Speed Control
- Default configuration is optimized, no adjustment needed
- If blocked, reduce `NUM_WORKERS` to 2-3

### 2. Data Quality
- ✅ 100% success rate extracting job descriptions
- ✅ Automatically handles Unicode and special characters
- ✅ Intelligently extracts email addresses

### 3. Legal Compliance
- ⚖️ For personal research and learning only
- ⚖️ Follow website robots.txt and terms of use
- ⚖️ Don't scrape too frequently

### 4. Excel Compatibility
The output CSV file uses UTF-8 BOM encoding and can be opened directly in Excel/WPS.

If you see extra rows, this is normal (job descriptions contain line breaks). The actual number of jobs is based on data rows.

## 🛠️ Troubleshooting

### ChromeDriver Error
```bash
pip install --upgrade webdriver-manager
```

### Element Not Found
Website structure may have updated, check CSS selectors:
- `article[data-automation="normalJob"]` (job cards)
- `div[data-automation="jobDescription"]` (job description)

### Session Expired
The scraper will automatically retry, no manual intervention needed.

### High Memory Usage
4 browsers will use ~2GB memory. If memory is insufficient:
```python
NUM_WORKERS = 2  # Reduce to 2 browsers
```

## 📂 Output Examples

The following files will be generated:
- `jobstreet_all_jobs.csv` - Raw data
- `jobstreet_final_merged_fixed.csv` - Deduplicated final data (recommended)

## 🎯 Project Goal

Scrape job listings from JobStreet Singapore. Default configuration is for telemarketing-related positions, but can be modified for any keywords:
- 📞 Telemarketing (default)
- 💼 Sales, Marketing, Customer Service
- 💻 IT, Software Engineering, Data Analysis
- 🏢 Or any other job type

See [Changing Search Keywords](#changing-search-keywords-) section above.

---

**© 2025 guofang | For educational and research purposes only**
