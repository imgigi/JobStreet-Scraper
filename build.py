"""
Build script - packages the scraper into a standalone .exe
Run: python build.py
"""

import subprocess
import sys


def main():
    print("=" * 60)
    print("Building JobStreet Scraper .exe")
    print("=" * 60)

    # Install PyInstaller if not present
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",            # Single .exe file
        "--windowed",           # No console window (GUI app)
        "--name", "JobStreetScraper",
        "--icon", "NONE",       # No custom icon
        "--add-data", "templates;templates",  # Include templates folder
        # Hidden imports that PyInstaller might miss
        "--hidden-import", "selenium",
        "--hidden-import", "selenium.webdriver",
        "--hidden-import", "selenium.webdriver.chrome",
        "--hidden-import", "selenium.webdriver.chrome.service",
        "--hidden-import", "selenium.webdriver.chrome.options",
        "--hidden-import", "webdriver_manager",
        "--hidden-import", "webdriver_manager.chrome",
        "--hidden-import", "bs4",
        "--hidden-import", "lxml",
        # Reduce size: exclude unnecessary modules
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
    print("Your .exe is at: dist/JobStreetScraper.exe")
    print("=" * 60)
    print("\nShare this file with users. They only need:")
    print("  1. Google Chrome installed")
    print("  2. Internet connection")
    print("That's it! Double-click to run.")


if __name__ == "__main__":
    main()
