"""
Build script for macOS - packages the scraper into a standalone .app
Run on a Mac: python3 build_mac.py
"""

import subprocess
import sys


def main():
    print("=" * 60)
    print("Building JobStreet Scraper for macOS")
    print("=" * 60)

    # Install dependencies
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "pyinstaller", "selenium", "beautifulsoup4",
                           "lxml", "webdriver-manager"])

    # Build command (macOS uses : as separator for --add-data)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "JobStreetScraper",
        "--add-data", "templates:templates",  # macOS uses : not ;
        "--hidden-import", "selenium",
        "--hidden-import", "selenium.webdriver",
        "--hidden-import", "selenium.webdriver.chrome",
        "--hidden-import", "selenium.webdriver.chrome.service",
        "--hidden-import", "selenium.webdriver.chrome.options",
        "--hidden-import", "webdriver_manager",
        "--hidden-import", "webdriver_manager.chrome",
        "--hidden-import", "bs4",
        "--hidden-import", "lxml",
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "--exclude-module", "PIL",
        "--exclude-module", "scipy",
        "--exclude-module", "torch",
        "app.py",
    ]

    print("\nRunning PyInstaller...\n")
    subprocess.check_call(cmd)

    print("\n" + "=" * 60)
    print("Build complete!")
    print("Your app is at: dist/JobStreetScraper")
    print("=" * 60)
    print("\nShare this file with Mac users. They only need:")
    print("  1. Google Chrome installed")
    print("  2. Internet connection")
    print("That's it! Double-click to run.")
    print("\nTip: If macOS blocks the app, go to")
    print('  System Settings > Privacy & Security > "Open Anyway"')


if __name__ == "__main__":
    main()
