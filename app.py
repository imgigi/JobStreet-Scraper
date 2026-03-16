"""
JobStreet Scraper - Web UI Application
Double-click to run, opens in your browser automatically!
"""

import sys
import io
import os
import time
import csv
import re
import json
import threading
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup


# ─── Scraper Logic ───

def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails[0] if emails else "Not available"


def get_job_description(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    desc_selectors = [
        'div[data-automation="jobDescription"]',
        'div[data-automation="jobAdDetails"]',
        'div[class*="jobDescription"]',
        'div[class*="job-description"]',
        'div[class*="JobDescription"]',
        'section[data-automation="jobDescription"]',
        'div[id*="jobDescription"]',
    ]

    for selector in desc_selectors:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            break
        except:
            continue

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(1.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for selector in desc_selectors:
        elem = soup.select_one(selector)
        if elem:
            text = elem.get_text(separator='\n', strip=True)
            if len(text) > 30:
                return text

    candidates = []
    for div in soup.find_all(['div', 'section']):
        text = div.get_text(separator='\n', strip=True)
        if 100 < len(text) < 5000:
            lower = text.lower()
            keywords = ['responsibilities', 'requirements', 'qualifications', 'experience',
                        'salary', 'benefits', 'job description', 'duties', 'skills']
            score = sum(1 for kw in keywords if kw in lower)
            if score >= 2:
                candidates.append((score, len(text), text))

    if candidates:
        candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return candidates[0][2]

    return ""


print_lock = threading.Lock()


def fetch_job_details(driver_id, driver, job_info, job_number, log_func):
    company_name = job_info['company_name']
    job_link = job_info['job_link']

    description = ""
    email = "Not available"
    status = "[--]"

    if job_link:
        try:
            description = get_job_description(driver, job_link)
            if description:
                email = extract_email(description)
            status = "[OK]" if len(description) > 30 else "[--]"
        except Exception as e:
            err_msg = str(e)
            if 'invalid session' in err_msg.lower():
                status = "[SESSION ERR]"
            else:
                status = "[ERR]"
    else:
        status = "[NO LINK]"

    with print_lock:
        log_func(f"{job_number:3d}. {company_name[:30]:30s} {status}")

    return {
        'company_name': company_name,
        'job_title': job_info['job_title'],
        'job_description': description,
        'email': email,
        'job_url': job_link if job_link else "N/A"
    }


# ─── Scraper Engine ───

class ScraperEngine:
    def __init__(self):
        self.logs = []
        self.running = False
        self.stop_flag = False
        self.status = "Ready"
        self.lock = threading.Lock()

    def log(self, msg):
        with self.lock:
            self.logs.append(msg)
            print(msg)

    def get_logs_since(self, index):
        with self.lock:
            return self.logs[index:]

    def run(self, url, num_workers, output_file):
        self.logs = []
        self.running = True
        self.stop_flag = False
        self.status = "Starting Chrome browsers..."
        fieldnames = ['company_name', 'job_title', 'job_description', 'email', 'job_url']

        self.log("JobStreet Scraper Starting...")
        self.log("=" * 60)

        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            self.log("Downloading/checking ChromeDriver...")
            service = Service(ChromeDriverManager().install())

            def make_driver():
                return webdriver.Chrome(service=service, options=chrome_options)

            driver = make_driver()
            detail_drivers = [make_driver() for _ in range(num_workers)]
            self.log(f"Created {num_workers + 1} browser instances\n")

        except Exception as e:
            self.log(f"\n[ERROR] Failed to start Chrome: {e}")
            self.log("\nMake sure Google Chrome is installed!")
            self.status = "Error - Chrome not found"
            self.running = False
            return

        existing_ok_urls = set()
        existing_all_urls = set()
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url_val = row.get('job_url', '')
                    existing_all_urls.add(url_val)
                    if len(row.get('job_description', '')) > 30:
                        existing_ok_urls.add(url_val)
            self.log(f"Resuming: found {len(existing_ok_urls)} existing jobs with descriptions")
        else:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

        total_count = len(existing_all_urls)
        page = 1

        try:
            while not self.stop_flag:
                page_url = url if page == 1 else f"{url}?page={page}"
                self.status = f"Scraping page {page}..."
                self.log(f"\n--- Page {page} ---")

                try:
                    driver.get(page_url)
                except Exception:
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = make_driver()
                    driver.get(page_url)

                wait = WebDriverWait(driver, 10)
                try:
                    wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'article[data-automation="normalJob"]')))
                except TimeoutException:
                    self.log("No job cards found, stopping.")
                    break

                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                cards = soup.select('article[data-automation="normalJob"]')

                if not cards:
                    self.log("No jobs on this page, stopping.")
                    break

                self.log(f"Found {len(cards)} jobs, fetching details...\n")

                jobs_to_fetch = []
                for card in cards:
                    company = card.select_one('[data-automation="jobCompany"]')
                    title = card.select_one('[data-automation="jobTitle"]')

                    company_name = company.get_text(strip=True) if company else "N/A"
                    job_title = title.get_text(strip=True) if title else "N/A"
                    job_link = title.get('href') if title and title.name == 'a' else None

                    if job_link and not job_link.startswith('http'):
                        job_link = f"https://sg.jobstreet.com{job_link}"

                    if job_link in existing_ok_urls:
                        total_count += 1
                        self.log(f"{total_count:3d}. {company_name[:30]:30s} [SKIP]")
                        continue

                    total_count += 1
                    jobs_to_fetch.append({
                        'company_name': company_name,
                        'job_title': job_title,
                        'job_link': job_link
                    })

                page_jobs = []
                start_num = total_count - len(jobs_to_fetch) + 1

                with ThreadPoolExecutor(max_workers=num_workers) as executor:
                    futures = []
                    for i, job_info in enumerate(jobs_to_fetch):
                        driver_idx = i % num_workers
                        job_number = start_num + i
                        future = executor.submit(
                            fetch_job_details,
                            driver_idx,
                            detail_drivers[driver_idx],
                            job_info,
                            job_number,
                            self.log
                        )
                        futures.append(future)

                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            page_jobs.append(result)
                        except Exception as e:
                            self.log(f"[ERROR in thread: {str(e)[:40]}]")

                if page_jobs:
                    with open(output_file, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerows(page_jobs)
                    self.log(f"  -> Saved {len(page_jobs)} jobs to CSV")

                try:
                    next_btn = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
                    if next_btn.is_enabled():
                        page += 1
                    else:
                        self.log("\nNo more pages.")
                        break
                except (NoSuchElementException, Exception):
                    self.log("\nReached last page.")
                    break

        finally:
            self.log("\nClosing browsers...")
            for d in detail_drivers:
                try:
                    d.quit()
                except:
                    pass
            try:
                driver.quit()
            except:
                pass

        if os.path.exists(output_file):
            seen = {}
            with open(output_file, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    url_val = row.get('job_url', '')
                    has_desc = len(row.get('job_description', '')) > 30
                    if url_val not in seen or (has_desc and len(seen[url_val].get('job_description', '')) <= 30):
                        seen[url_val] = row

            rows = list(seen.values())
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            ok = sum(1 for r in rows if len(r.get('job_description', '')) > 30)
            self.log(f"\n{'=' * 60}")
            self.log(f"Done: {ok}/{len(rows)} unique jobs got descriptions")
            self.log(f"Saved to {output_file}")
            self.log(f"{'=' * 60}")
            self.status = f"Done! {ok}/{len(rows)} jobs saved to {output_file}"

        self.running = False


# ─── Web UI ───

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JobStreet Scraper</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         background: #f0f2f5; color: #333; padding: 20px; }
  .container { max-width: 750px; margin: 0 auto; }
  h1 { text-align: center; margin-bottom: 20px; color: #1a73e8; }
  .card { background: #fff; border-radius: 10px; padding: 20px; margin-bottom: 15px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  .card h2 { font-size: 16px; margin-bottom: 12px; color: #555; }
  label { display: block; font-size: 13px; color: #666; margin-bottom: 4px; }
  input[type=text], input[type=number] {
    width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px;
    font-size: 14px; margin-bottom: 10px; }
  input:focus { outline: none; border-color: #1a73e8; }
  .row { display: flex; gap: 15px; }
  .row > div { flex: 1; }
  .buttons { display: flex; gap: 10px; margin-bottom: 15px; }
  button { padding: 10px 24px; border: none; border-radius: 6px; font-size: 14px;
           cursor: pointer; font-weight: 600; }
  #startBtn { background: #1a73e8; color: #fff; }
  #startBtn:hover { background: #1557b0; }
  #startBtn:disabled { background: #94b8e8; cursor: not-allowed; }
  #stopBtn { background: #ea4335; color: #fff; }
  #stopBtn:hover { background: #c5221f; }
  #stopBtn:disabled { background: #e8a09b; cursor: not-allowed; }
  .status { font-weight: 600; font-size: 15px; color: #1a73e8; margin-bottom: 10px; }
  #log { background: #1e1e1e; color: #d4d4d4; font-family: 'Consolas', 'Courier New', monospace;
         font-size: 12px; padding: 12px; border-radius: 8px; height: 350px;
         overflow-y: auto; white-space: pre-wrap; word-break: break-all; }
  .ok { color: #4caf50; }
  .err { color: #ef5350; }
  .skip { color: #ffa726; }
</style>
</head>
<body>
<div class="container">
  <h1>JobStreet Scraper</h1>
  <div class="card">
    <h2>Settings</h2>
    <label>Search URL</label>
    <input type="text" id="url" value="https://sg.jobstreet.com/telemarketing-jobs">
    <div class="row">
      <div>
        <label>Concurrent browsers</label>
        <input type="number" id="workers" value="4" min="1" max="8">
      </div>
      <div>
        <label>Output file</label>
        <input type="text" id="output" value="jobstreet_all_jobs.csv">
      </div>
    </div>
  </div>
  <div class="buttons">
    <button id="startBtn" onclick="startScraping()">Start Scraping</button>
    <button id="stopBtn" onclick="stopScraping()" disabled>Stop</button>
  </div>
  <div class="status" id="status">Ready</div>
  <div class="card">
    <h2>Log</h2>
    <div id="log"></div>
  </div>
</div>
<script>
let polling = null;
let logIndex = 0;

function startScraping() {
  const url = document.getElementById('url').value;
  const workers = document.getElementById('workers').value;
  const output = document.getElementById('output').value;
  document.getElementById('startBtn').disabled = true;
  document.getElementById('stopBtn').disabled = false;
  document.getElementById('log').innerHTML = '';
  logIndex = 0;

  fetch('/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url, workers: parseInt(workers), output})
  });

  polling = setInterval(pollLogs, 500);
}

function stopScraping() {
  fetch('/stop', {method: 'POST'});
  document.getElementById('status').textContent = 'Stopping after current page...';
}

function pollLogs() {
  fetch('/logs?since=' + logIndex)
    .then(r => r.json())
    .then(data => {
      const el = document.getElementById('log');
      data.logs.forEach(line => {
        const span = document.createElement('span');
        if (line.includes('[OK]')) span.className = 'ok';
        else if (line.includes('[ERR') || line.includes('[SESSION ERR]')) span.className = 'err';
        else if (line.includes('[SKIP]')) span.className = 'skip';
        span.textContent = line + '\\n';
        el.appendChild(span);
      });
      logIndex += data.logs.length;
      if (data.logs.length > 0) el.scrollTop = el.scrollHeight;
      document.getElementById('status').textContent = data.status;
      if (!data.running) {
        clearInterval(polling);
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
      }
    });
}
</script>
</body>
</html>"""

engine = ScraperEngine()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        elif self.path.startswith('/logs'):
            since = 0
            if '?' in self.path:
                qs = parse_qs(self.path.split('?')[1])
                since = int(qs.get('since', [0])[0])
            data = {
                'logs': engine.get_logs_since(since),
                'status': engine.status,
                'running': engine.running
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/start':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            url = body.get('url', 'https://sg.jobstreet.com/telemarketing-jobs')
            workers = body.get('workers', 4)
            output = body.get('output', 'jobstreet_all_jobs.csv')

            if not engine.running:
                thread = threading.Thread(target=engine.run, args=(url, workers, output), daemon=True)
                thread.start()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

        elif self.path == '/stop':
            engine.stop_flag = True
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

    def log_message(self, format, *args):
        pass  # Suppress HTTP request logs


def main():
    port = 8899
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f"JobStreet Scraper running at http://127.0.0.1:{port}")
    print("Opening browser...")
    webbrowser.open(f'http://127.0.0.1:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
