#!/usr/bin/env python3
"""
Paper Fast Scan — Quick Install
================================
Install dependencies for the Paper-Fast-Scan skill.
Run: python install.py
"""

import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("  Paper Fast Scan — Installer")
    print("=" * 50)

    # 1. Check Python
    print(f"\n[1/3] Python: {sys.version}")

    # 2. Install pip dependencies
    print("\n[2/3] Installing pip packages (pymupdf, pdfplumber, pillow)...")
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])

    # 3. Verify
    print("\n[3/3] Verifying installation...")
    try:
        import fitz
        print(f"  ✓ pymupdf {fitz.version[0]}")
    except ImportError:
        print("  ✗ pymupdf failed to import")

    try:
        import pdfplumber
        print("  ✓ pdfplumber")
    except ImportError:
        print("  ✗ pdfplumber failed to import")

    try:
        from PIL import Image
        print("  ✓ pillow (PIL)")
    except ImportError:
        print("  ✗ pillow failed to import")

    print("\n" + "=" * 50)
    print("  Installation complete!")
    print("=" * 50)
    print(f"\n  Templates: {os.path.join(os.path.dirname(__file__), 'templates')}")
    print(f"  Examples:  {os.path.join(os.path.dirname(__file__), 'examples')}")
    print("\n  Usage: tell your Hermes Agent to 'parse this PDF with Paper-Fast-Scan'")
    print()

if __name__ == "__main__":
    main()
