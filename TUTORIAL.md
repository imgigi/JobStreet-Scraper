# 📚 JobStreet 爬虫 - 新手完整教程

**作者**: guofang

本教程将从零开始，手把手教你如何使用这个爬虫工具。即使你完全不懂编程，也能轻松上手！

---

## 📋 目录

- [第一步：安装 Python](#第一步安装-python)
- [第二步：安装 Chrome 浏览器](#第二步安装-chrome-浏览器)
- [第三步：下载项目文件](#第三步下载项目文件)
- [第四步：打开命令行](#第四步打开命令行)
- [第五步：进入项目目录](#第五步进入项目目录)
- [第六步：安装依赖包](#第六步安装依赖包)
- [第七步：运行爬虫](#第七步运行爬虫)
- [第八步：查看结果](#第八步查看结果)
- [第九步：修改搜索关键词（可选）](#第九步修改搜索关键词可选)
- [常见问题解答](#常见问题解答)

---

## 第一步：安装 Python

### Windows 系统

1. **下载 Python**
   - 访问 Python 官网：https://www.python.org/downloads/
   - 点击黄色按钮 "Download Python 3.x.x"（3.8 或更高版本均可）
   - 下载完成后，双击安装包

2. **安装 Python**
   - ⚠️ **重要**：安装时，务必勾选 **"Add Python to PATH"**（这个很重要！）
   - 点击 "Install Now"
   - 等待安装完成

3. **验证安装**
   - 按下 `Win + R` 键
   - 输入 `cmd` 并回车
   - 在黑色窗口中输入：
     ```bash
     python --version
     ```
   - 如果显示 `Python 3.x.x`，说明安装成功！

### Mac 系统

1. **下载 Python**
   - 访问：https://www.python.org/downloads/
   - 下载 macOS 版本
   - 双击 `.pkg` 文件安装

2. **验证安装**
   - 打开 "终端" (Terminal)
   - 输入：
     ```bash
     python3 --version
     ```
   - 如果显示版本号，说明安装成功！

---

## 第二步：安装 Chrome 浏览器

1. 访问：https://www.google.com/chrome/
2. 下载并安装 Google Chrome
3. 安装完成后，打开一次 Chrome 确保正常运行

**为什么需要 Chrome？**
爬虫需要用 Chrome 浏览器自动访问网站，模拟人类浏览行为。

---

## 第三步：下载项目文件

### 方法 1：如果你有压缩包

1. 解压下载的 `.zip` 文件到任意位置
2. 记住解压的文件夹路径（比如：`C:\Users\你的用户名\Desktop\jobstreet_scraper`）

### 方法 2：如果使用 Git（高级用户）

```bash
git clone <项目地址>
cd jobstreet_scraper
```

---

## 第四步：打开命令行

### Windows

**方法 A（推荐）：**
1. 打开文件资源管理器
2. 进入项目文件夹（就是包含 `jobstreet_scraper.py` 的那个文件夹）
3. 在文件夹空白处按住 `Shift` 键 + 右键点击
4. 选择 "在此处打开 PowerShell 窗口" 或 "在此处打开命令窗口"

**方法 B：**
1. 按 `Win + R`
2. 输入 `cmd` 并回车
3. 继续看第五步

### Mac

1. 打开 "终端" (Terminal)
   - 按 `Command + 空格`，输入 "Terminal" 并回车
2. 继续看第五步

---

## 第五步：进入项目目录

如果你用方法 A 打开的命令行，可以跳过这一步。

如果你用方法 B，需要手动进入项目文件夹：

### Windows 示例

```bash
cd C:\Users\你的用户名\Desktop\jobstreet_scraper
```

### Mac 示例

```bash
cd ~/Desktop/jobstreet_scraper
```

**小技巧**：可以直接把文件夹拖到命令行窗口中，会自动填入路径！

**验证**：输入 `dir`（Windows）或 `ls`（Mac）查看文件，应该能看到 `jobstreet_scraper.py`。

---

## 第六步：安装依赖包

现在需要安装爬虫需要的工具包。

### Windows

在命令行中输入：

```bash
pip install -r requirements.txt
```

### Mac

```bash
pip3 install -r requirements.txt
```

**等待安装**：会看到一堆文字滚动，这是正常的！等待几分钟直到看到 "Successfully installed..."。

### 如果遇到错误

如果提示 `pip: command not found` 或 `'pip' 不是内部或外部命令`：

**Windows：**
```bash
python -m pip install -r requirements.txt
```

**Mac：**
```bash
python3 -m pip install -r requirements.txt
```

---

## 第七步：运行爬虫

终于到激动人心的时刻了！

### Windows

```bash
python jobstreet_scraper.py
```

### Mac

```bash
python3 jobstreet_scraper.py
```

### 你会看到什么？

1. **初始化**：显示 "Created 4 concurrent browsers..."
2. **开始爬取**：每爬一个职位会显示一行，例如：
   ```
   --- Page 1 ---
   Found 30 jobs, fetching details with 4 concurrent browsers...

     1. PERSOL                         [OK]
     2. DBS Bank                       [OK]
     3. Singtel                        [OK]
   ```
3. **进度提示**：每 100 个职位会显示进度
4. **自动保存**：每一页爬完自动保存到 CSV 文件

### ⏱️ 需要多久？

- 每页大约 10-15 秒
- 如果有 25 页，大约 3-5 分钟完成

### 如何停止？

- 按 `Ctrl + C`（Windows/Mac 都一样）
- 不用担心数据丢失，下次重新运行会从断点继续！

---

## 第八步：查看结果

爬虫运行完成后，会在项目文件夹中生成 CSV 文件。

### 找到 CSV 文件

在项目文件夹中找到：
- `jobstreet_all_jobs.csv` - 这就是爬取的数据

### 打开 CSV 文件

**方法 1：用 Excel 打开**
1. 右键点击 `jobstreet_all_jobs.csv`
2. 选择 "打开方式" → "Microsoft Excel"

**方法 2：用 WPS 打开**
1. 双击 CSV 文件
2. 选择用 WPS 表格打开

**方法 3：用记事本查看（不推荐）**
- 会看到乱码和不整齐的数据

### CSV 文件包含什么？

| 列名 | 说明 |
|------|------|
| company_name | 公司名称 |
| job_title | 职位名称 |
| job_description | 完整的职位描述 |
| email | 邮箱地址（如果有） |
| job_url | 职位链接 |

---

## 第九步：修改搜索关键词（可选）

如果想爬取其他职位（不只是 telemarketing），按照以下步骤操作：

### 1. 打开代码文件

用记事本或任何文本编辑器打开 `jobstreet_scraper.py`

**推荐编辑器：**
- 记事本（Windows 自带）
- VS Code（专业，免费）
- Notepad++（轻量，免费）

### 2. 找到第 145 行

按 `Ctrl + G`（或 `Cmd + G` on Mac）跳到第 145 行，找到：

```python
url = "https://sg.jobstreet.com/telemarketing-jobs"
```

### 3. 修改 URL

将 URL 改成你想搜索的关键词，例如：

```python
# 搜索销售职位
url = "https://sg.jobstreet.com/sales-jobs"

# 搜索市场营销职位
url = "https://sg.jobstreet.com/marketing-jobs"

# 搜索软件工程师职位
url = "https://sg.jobstreet.com/software-engineer-jobs"
```

### 4. 修改输出文件名（建议）

找到第 170 行，修改文件名避免覆盖之前的数据：

```python
output_file = 'jobstreet_sales_jobs.csv'  # 改成对应的名字
```

### 5. 保存并重新运行

- 按 `Ctrl + S` 保存
- 关闭编辑器
- 重新运行爬虫（回到第七步）

---

## 常见问题解答

### ❓ Q1: 提示 "python 不是内部或外部命令"

**原因**：Python 没有添加到系统 PATH。

**解决方法**：
1. 卸载 Python
2. 重新安装，记得勾选 "Add Python to PATH"
3. 或者使用完整路径运行：
   ```bash
   C:\Users\你的用户名\AppData\Local\Programs\Python\Python311\python.exe jobstreet_scraper.py
   ```

### ❓ Q2: 安装依赖时报错 "error: Microsoft Visual C++ 14.0 is required"

**解决方法**：
1. 下载并安装 Visual C++ 运行库：https://aka.ms/vs/17/release/vc_redist.x64.exe
2. 重新运行安装命令

### ❓ Q3: 爬虫运行一半就停止了

**原因可能是**：
- 网络问题
- 浏览器会话过期
- 网站反爬虫

**解决方法**：
- 直接重新运行爬虫，会自动从断点继续
- 如果反复失败，可以减少并发数（修改代码第 166 行）：
  ```python
  NUM_WORKERS = 2  # 从 4 改成 2
  ```

### ❓ Q4: CSV 文件打开后中文显示乱码

**解决方法**：
1. 用 Excel 打开 CSV 时，选择 "数据" → "从文本/CSV"
2. 选择编码为 "UTF-8"
3. 点击加载

### ❓ Q5: 提示 "chromedriver" 相关错误

**原因**：ChromeDriver 下载失败。

**解决方法**：
```bash
pip install --upgrade webdriver-manager
```

然后重新运行爬虫。

### ❓ Q6: 爬虫速度太慢或太快

**太慢**：增加并发数
```python
NUM_WORKERS = 6  # 改成 6 或 8（注意内存）
```

**太快被封**：减少并发数
```python
NUM_WORKERS = 2  # 改成 2
```

### ❓ Q7: 想要暂停爬虫

- 按 `Ctrl + C` 停止
- 数据已经保存到 CSV
- 下次运行会自动跳过已爬取的职位

### ❓ Q8: 如何完全重新开始爬取

```bash
# 删除旧的 CSV 文件
del jobstreet_all_jobs.csv     # Windows
rm jobstreet_all_jobs.csv      # Mac

# 重新运行
python jobstreet_scraper.py
```

### ❓ Q9: 可以同时爬取多个关键词吗？

可以！方法如下：

1. 复制一份 `jobstreet_scraper.py`，命名为 `jobstreet_scraper_sales.py`
2. 修改第 145 行的 URL 和第 170 行的输出文件名
3. 打开两个命令行窗口，分别运行两个脚本

**但不建议**：会占用大量内存（每个脚本 4 个浏览器）。

### ❓ Q10: 这合法吗？会被封吗？

- ⚖️ **法律**：仅用于个人学习和研究，不要商业使用
- 🛡️ **封禁风险**：
  - 爬虫已经模拟正常用户行为
  - 速度控制合理，一般不会被封
  - 如果担心，可以减少 `NUM_WORKERS` 到 2

---

## 🎉 恭喜完成！

如果你完成了所有步骤，说明你已经成功：
- ✅ 配置了 Python 环境
- ✅ 安装了所有依赖
- ✅ 运行了你的第一个爬虫
- ✅ 获取了 JobStreet 的职位数据

**下一步可以做什么？**
- 📊 用 Excel 分析数据，找出哪些公司在招人
- 📧 联系有邮箱的公司投递简历
- 🔍 尝试不同的搜索关键词
- 🚀 学习修改代码，添加更多功能

---

## 💡 进阶学习

如果你想深入了解：

1. **Python 基础**：
   - 廖雪峰的 Python 教程：https://www.liaoxuefeng.com/wiki/1016959663602400

2. **网络爬虫**：
   - Selenium 官方文档：https://selenium-python.readthedocs.io/

3. **数据处理**：
   - pandas 教程（处理 CSV）：https://pandas.pydata.org/docs/

---

## 📞 需要帮助？

如果遇到本教程未覆盖的问题：

1. 仔细阅读错误信息（红色文字）
2. 复制错误信息到 Google 搜索
3. 查看项目的 `README_SCRAPER.md` 获取更多技术细节

---

**© 2025 guofang | 祝你使用愉快！**
