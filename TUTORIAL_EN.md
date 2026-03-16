# 📚 JobStreet Scraper - Complete Beginner's Tutorial

**Author**: guofang

This tutorial will guide you step-by-step from zero to hero. Even if you have no programming experience, you can easily use this tool!

---

## 📋 Table of Contents

- [Step 1: Install Python](#step-1-install-python)
- [Step 2: Install Chrome Browser](#step-2-install-chrome-browser)
- [Step 3: Download Project Files](#step-3-download-project-files)
- [Step 4: Open Command Line](#step-4-open-command-line)
- [Step 5: Navigate to Project Directory](#step-5-navigate-to-project-directory)
- [Step 6: Install Dependencies](#step-6-install-dependencies)
- [Step 7: Run the Scraper](#step-7-run-the-scraper)
- [Step 8: View Results](#step-8-view-results)
- [Step 9: Change Search Keywords (Optional)](#step-9-change-search-keywords-optional)
- [FAQ](#faq)

---

## Step 1: Install Python

### Windows

1. **Download Python**
   - Visit: https://www.python.org/downloads/
   - Click the yellow button "Download Python 3.x.x" (version 3.8 or higher)
   - After download completes, double-click the installer

2. **Install Python**
   - ⚠️ **IMPORTANT**: During installation, CHECK the box **"Add Python to PATH"** (very important!)
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**
   - Press `Win + R`
   - Type `cmd` and press Enter
   - In the black window, type:
     ```bash
     python --version
     ```
   - If you see `Python 3.x.x`, installation was successful!

### Mac

1. **Download Python**
   - Visit: https://www.python.org/downloads/
   - Download macOS version
   - Double-click the `.pkg` file to install

2. **Verify Installation**
   - Open "Terminal"
   - Type:
     ```bash
     python3 --version
     ```
   - If you see a version number, installation was successful!

---

## Step 2: Install Chrome Browser

1. Visit: https://www.google.com/chrome/
2. Download and install Google Chrome
3. After installation, open Chrome once to ensure it works properly

**Why do I need Chrome?**
The scraper uses Chrome to automatically visit websites and simulate human browsing behavior.

---

## Step 3: Download Project Files

### Method 1: If you have a zip file

1. Extract the downloaded `.zip` file to any location
2. Remember the extracted folder path (e.g., `C:\Users\YourName\Desktop\jobstreet_scraper`)

### Method 2: If using Git (Advanced users)

```bash
git clone <project-url>
cd jobstreet_scraper
```

---

## Step 4: Open Command Line

### Windows

**Method A (Recommended):**
1. Open File Explorer
2. Navigate to the project folder (the one containing `jobstreet_scraper.py`)
3. Hold `Shift` key and right-click in an empty area
4. Select "Open PowerShell window here" or "Open command window here"

**Method B:**
1. Press `Win + R`
2. Type `cmd` and press Enter
3. Continue to Step 5

### Mac

1. Open "Terminal"
   - Press `Command + Space`, type "Terminal" and press Enter
2. Continue to Step 5

---

## Step 5: Navigate to Project Directory

If you used Method A to open the command line, you can skip this step.

If you used Method B, you need to manually navigate to the project folder:

### Windows Example

```bash
cd C:\Users\YourName\Desktop\jobstreet_scraper
```

### Mac Example

```bash
cd ~/Desktop/jobstreet_scraper
```

**Pro Tip**: You can drag the folder directly into the command line window to auto-fill the path!

**Verify**: Type `dir` (Windows) or `ls` (Mac) to view files. You should see `jobstreet_scraper.py`.

---

## Step 6: Install Dependencies

Now we need to install the required packages for the scraper.

### Windows

In the command line, type:

```bash
pip install -r requirements.txt
```

### Mac

```bash
pip3 install -r requirements.txt
```

**Wait for Installation**: You'll see lots of text scrolling - this is normal! Wait a few minutes until you see "Successfully installed...".

### If you encounter errors

If you see `pip: command not found` or `'pip' is not recognized`:

**Windows:**
```bash
python -m pip install -r requirements.txt
```

**Mac:**
```bash
python3 -m pip install -r requirements.txt
```

---

## Step 7: Run the Scraper

Finally, the exciting moment!

### Windows

```bash
python jobstreet_scraper.py
```

### Mac

```bash
python3 jobstreet_scraper.py
```

### What will you see?

1. **Initialization**: Shows "Created 4 concurrent browsers..."
2. **Start Scraping**: Each job scraped shows a line, like:
   ```
   --- Page 1 ---
   Found 30 jobs, fetching details with 4 concurrent browsers...

     1. PERSOL                         [OK]
     2. DBS Bank                       [OK]
     3. Singtel                        [OK]
   ```
3. **Progress Updates**: Every 100 jobs shows progress
4. **Auto-save**: Automatically saves to CSV after each page

### ⏱️ How long does it take?

- About 10-15 seconds per page
- If there are 25 pages, approximately 3-5 minutes total

### How to stop?

- Press `Ctrl + C` (same for Windows/Mac)
- Don't worry about data loss - next run will resume from where you left off!

---

## Step 8: View Results

After the scraper completes, a CSV file will be generated in the project folder.

### Find the CSV file

In the project folder, look for:
- `jobstreet_all_jobs.csv` - This is your scraped data

### Open the CSV file

**Method 1: Open with Excel**
1. Right-click `jobstreet_all_jobs.csv`
2. Select "Open with" → "Microsoft Excel"

**Method 2: Open with Google Sheets**
1. Go to Google Sheets
2. File → Import → Upload the CSV file

**Method 3: Open with Notepad (Not recommended)**
- You'll see messy, unformatted data

### What's in the CSV file?

| Column | Description |
|--------|-------------|
| company_name | Company name |
| job_title | Job title |
| job_description | Full job description |
| email | Email address (if available) |
| job_url | Job link |

---

## Step 9: Change Search Keywords (Optional)

If you want to scrape jobs other than telemarketing, follow these steps:

### 1. Open the code file

Use Notepad or any text editor to open `jobstreet_scraper.py`

**Recommended Editors:**
- Notepad (Windows built-in)
- TextEdit (Mac built-in)
- VS Code (Professional, free)
- Sublime Text (Lightweight, free)

### 2. Find line 145

Press `Ctrl + G` (or `Cmd + G` on Mac) to jump to line 145, find:

```python
url = "https://sg.jobstreet.com/telemarketing-jobs"
```

### 3. Modify the URL

Change the URL to your desired search keyword, for example:

```python
# Search for sales jobs
url = "https://sg.jobstreet.com/sales-jobs"

# Search for marketing jobs
url = "https://sg.jobstreet.com/marketing-jobs"

# Search for software engineer jobs
url = "https://sg.jobstreet.com/software-engineer-jobs"
```

### 4. Modify output filename (Recommended)

Find line 170, change the filename to avoid overwriting previous data:

```python
output_file = 'jobstreet_sales_jobs.csv'  # Change to corresponding name
```

### 5. Save and re-run

- Press `Ctrl + S` to save
- Close the editor
- Re-run the scraper (go back to Step 7)

---

## FAQ

### ❓ Q1: Error "python is not recognized as an internal or external command"

**Reason**: Python was not added to system PATH.

**Solution**:
1. Uninstall Python
2. Reinstall, remember to check "Add Python to PATH"
3. Or use the full path:
   ```bash
   C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe jobstreet_scraper.py
   ```

### ❓ Q2: Error during installation "error: Microsoft Visual C++ 14.0 is required"

**Solution**:
1. Download and install Visual C++ runtime: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Re-run the installation command

### ❓ Q3: Scraper stops halfway

**Possible reasons**:
- Network issues
- Browser session expired
- Website anti-scraping measures

**Solution**:
- Simply re-run the scraper, it will automatically resume
- If it fails repeatedly, reduce concurrency (modify line 166):
  ```python
  NUM_WORKERS = 2  # Change from 4 to 2
  ```

### ❓ Q4: CSV file shows garbled Chinese characters

**Solution**:
1. In Excel, go to "Data" → "From Text/CSV"
2. Select encoding as "UTF-8"
3. Click Load

### ❓ Q5: "chromedriver" related error

**Reason**: ChromeDriver download failed.

**Solution**:
```bash
pip install --upgrade webdriver-manager
```

Then re-run the scraper.

### ❓ Q6: Scraper too slow or too fast

**Too slow**: Increase concurrency
```python
NUM_WORKERS = 6  # Change to 6 or 8 (watch memory usage)
```

**Too fast, getting blocked**: Reduce concurrency
```python
NUM_WORKERS = 2  # Change to 2
```

### ❓ Q7: Want to pause the scraper

- Press `Ctrl + C` to stop
- Data is already saved to CSV
- Next run will automatically skip scraped jobs

### ❓ Q8: How to completely start over

```bash
# Delete old CSV file
del jobstreet_all_jobs.csv     # Windows
rm jobstreet_all_jobs.csv      # Mac

# Re-run
python jobstreet_scraper.py
```

### ❓ Q9: Can I scrape multiple keywords simultaneously?

Yes! Here's how:

1. Copy `jobstreet_scraper.py`, name it `jobstreet_scraper_sales.py`
2. Modify line 145 URL and line 170 output filename
3. Open two command line windows, run both scripts separately

**Not recommended**: Uses lots of memory (4 browsers per script).

### ❓ Q10: Is this legal? Will I get banned?

- ⚖️ **Legal**: For personal learning and research only, don't use commercially
- 🛡️ **Ban risk**:
  - The scraper simulates normal user behavior
  - Speed is controlled reasonably, usually won't get banned
  - If worried, reduce `NUM_WORKERS` to 2

---

## 🎉 Congratulations!

If you've completed all steps, you have successfully:
- ✅ Set up Python environment
- ✅ Installed all dependencies
- ✅ Run your first web scraper
- ✅ Obtained JobStreet job data

**What's next?**
- 📊 Analyze data in Excel, find companies hiring
- 📧 Contact companies with emails to submit resumes
- 🔍 Try different search keywords
- 🚀 Learn to modify code, add more features

---

## 💡 Advanced Learning

If you want to dive deeper:

1. **Python Basics**:
   - Python.org Tutorial: https://docs.python.org/3/tutorial/

2. **Web Scraping**:
   - Selenium Documentation: https://selenium-python.readthedocs.io/

3. **Data Processing**:
   - pandas Tutorial (CSV processing): https://pandas.pydata.org/docs/

---

## 📞 Need Help?

If you encounter issues not covered in this tutorial:

1. Carefully read the error message (red text)
2. Copy the error message and search on Google
3. Check the project's `README_SCRAPER.md` for more technical details

---

**© 2025 guofang | Happy scraping!**
