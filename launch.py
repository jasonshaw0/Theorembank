#!/usr/bin/env python3
"""
Quick launch script for the Formula Reference website.
Builds the site and opens it in the default browser.
"""

import subprocess
import webbrowser
import pathlib
import time

def main():
    print("🧮 Building Formula Reference website...")
    
    # Build the website
    result = subprocess.run(["python", "build.py"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Build failed:")
        print(result.stderr)
        return
    
    print(result.stdout)
    
    # Open in browser
    dist_path = pathlib.Path("dist/math/index.html").resolve()
    if dist_path.exists():
        print(f"🚀 Opening {dist_path} in browser...")
        webbrowser.open(f"file://{dist_path}")
    else:
        print("❌ Generated file not found!")

if __name__ == "__main__":
    main() 