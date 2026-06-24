#!/usr/bin/env python3
"""
Add sources to a NotebookLM notebook via browser automation.
Supports: URL, text paste, and file upload.
"""

import argparse
import sys
import re
import time
from pathlib import Path

# Import from base notebooklm skill
BASE_SKILL_DIR = Path.home() / ".claude" / "skills" / "notebooklm"
sys.path.insert(0, str(BASE_SKILL_DIR / "scripts"))

from patchright.sync_api import sync_playwright
from auth_manager import AuthManager
from notebook_manager import NotebookLibrary
from browser_utils import BrowserFactory, StealthUtils


# "Add source" button selectors
ADD_SOURCE_SELECTORS = [
    'button[aria-label*="Add source"]',
    'button[aria-label*="add source"]',
    'button[aria-label*="Add Source"]',
    'button[aria-label*="Upload"]',
    '[data-test-id="add-source"]',
    'button:has-text("Add source")',
    'button:has-text("Add Source")',
    'button:has-text("Upload")',
    'a[aria-label*="Add source"]',
    '.add-source-button',
]

# Source type option selectors (URL, text, file)
SOURCE_TYPE_URL_SELECTORS = [
    'button[aria-label*="URL"]',
    'button[aria-label*="Website"]',
    'button:has-text("URL")',
    'button:has-text("Website")',
    'a:has-text("URL")',
    '[data-test-id="source-url"]',
]

SOURCE_TYPE_TEXT_SELECTORS = [
    'button[aria-label*="Paste text"]',
    'button[aria-label*="Text"]',
    'button[aria-label*="Copy paste"]',
    'button:has-text("Paste text")',
    'button:has-text("Text")',
    '[data-test-id="source-text"]',
]

SOURCE_TYPE_FILE_SELECTORS = [
    'button[aria-label*="Upload"]',
    'button[aria-label*="File"]',
    'button[aria-label*="PDF"]',
    'button:has-text("Upload")',
    'button:has-text("File")',
    'input[type="file"]',
    '[data-test-id="source-file"]',
]

# URL input selectors
URL_INPUT_SELECTORS = [
    'input[aria-label*="URL"]',
    'input[aria-label*="url"]',
    'input[placeholder*="URL"]',
    'input[placeholder*="url"]',
    'input[placeholder*="Website"]',
    'input[type="url"]',
    '[data-test-id="url-input"] input',
]

# Text input selectors
TEXT_INPUT_SELECTORS = [
    'textarea[aria-label*="text"]',
    'textarea[aria-label*="Text"]',
    'textarea[placeholder*="Paste"]',
    'textarea[placeholder*="Enter text"]',
    '[data-test-id="text-input"] textarea',
]

# File input selector
FILE_INPUT_SELECTORS = [
    'input[type="file"]',
    'input[accept*=".pdf"]',
    'input[accept*=".txt"]',
    '[data-test-id="file-input"] input',
]

# Submit/confirm button after entering source
SUBMIT_SELECTORS = [
    'button[aria-label*="Insert"]',
    'button[aria-label*="Add"]',
    'button[aria-label*="Submit"]',
    'button:has-text("Insert")',
    'button:has-text("Add")',
    'button:has-text("Submit")',
    'button:has-text("Upload")',
]


def _resolve_notebook_url(notebook_url=None, notebook_id=None):
    """Resolve notebook URL from args or library."""
    if notebook_url:
        return notebook_url

    library = NotebookLibrary()

    if notebook_id:
        nb = library.get_notebook(notebook_id)
        if nb:
            return nb["url"]
        print(f"Notebook '{notebook_id}' not found")
        return None

    active = library.get_active_notebook()
    if active:
        print(f"Using active notebook: {active['name']}")
        return active["url"]

    print("No notebook specified and no active notebook")
    return None


def add_url_source(notebook_url: str, url: str, headless: bool = True) -> dict:
    """Add a URL as a source to a notebook."""
    auth = AuthManager()
    if not auth.is_authenticated():
        return {"status": "error", "message": "Not authenticated"}

    print(f"Adding URL source: {url}")
    print(f"  Notebook: {notebook_url}")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        page = context.new_page()

        page.goto(notebook_url, wait_until="domcontentloaded")
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=15000)
        StealthUtils.random_delay(1500, 2500)

        # Click "Add source"
        print("  Looking for 'Add source' button...")
        clicked = False
        for selector in ADD_SOURCE_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            try:
                page.click('text=/Add source|Upload|Add Source/i', timeout=3000)
                clicked = True
            except Exception:
                pass

        if not clicked:
            return {"status": "error", "message": "Could not find 'Add source' button"}

        StealthUtils.random_delay(1000, 1500)

        # Click "Website/URL" option
        print("  Selecting URL source type...")
        url_type_clicked = False
        for selector in SOURCE_TYPE_URL_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    url_type_clicked = True
                    break
            except Exception:
                continue

        if not url_type_clicked:
            try:
                page.click('text=/URL|Website|Link/i', timeout=3000)
                url_type_clicked = True
            except Exception:
                pass

        StealthUtils.random_delay(500, 1000)

        # Enter URL
        print("  Entering URL...")
        for selector in URL_INPUT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    el.click()
                    el.fill(url)
                    break
            except Exception:
                continue

        StealthUtils.random_delay(500, 1000)

        # Submit
        print("  Submitting...")
        for selector in SUBMIT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=2000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    break
            except Exception:
                continue
        else:
            page.keyboard.press("Enter")

        # Wait for source to be processed
        print("  Waiting for source processing...")
        StealthUtils.random_delay(3000, 5000)

        return {
            "status": "success",
            "source_type": "url",
            "source": url,
            "notebook_url": notebook_url,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        if context:
            try:
                context.close()
            except Exception:
                pass
        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass


def add_text_source(notebook_url: str, title: str, text: str, headless: bool = True) -> dict:
    """Add a text passage as a source to a notebook."""
    auth = AuthManager()
    if not auth.is_authenticated():
        return {"status": "error", "message": "Not authenticated"}

    print(f"Adding text source: {title}")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        page = context.new_page()

        page.goto(notebook_url, wait_until="domcontentloaded")
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=15000)
        StealthUtils.random_delay(1500, 2500)

        # Click "Add source"
        print("  Looking for 'Add source' button...")
        clicked = False
        for selector in ADD_SOURCE_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            try:
                page.click('text=/Add source|Upload/i', timeout=3000)
                clicked = True
            except Exception:
                pass

        StealthUtils.random_delay(1000, 1500)

        # Click "Paste text" option
        print("  Selecting text source type...")
        for selector in SOURCE_TYPE_TEXT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    break
            except Exception:
                continue
        else:
            try:
                page.click('text=/Paste text|Text/i', timeout=3000)
            except Exception:
                pass

        StealthUtils.random_delay(500, 1000)

        # Enter title
        print("  Entering title...")
        title_selectors = [
            'input[aria-label*="title"]',
            'input[aria-label*="Title"]',
            'input[placeholder*="title"]',
            'input[placeholder*="Title"]',
        ]
        for selector in title_selectors:
            try:
                el = page.wait_for_selector(selector, timeout=2000, state="visible")
                if el:
                    el.click()
                    el.fill(title)
                    break
            except Exception:
                continue

        StealthUtils.random_delay(300, 500)

        # Enter text
        print("  Entering text content...")
        for selector in TEXT_INPUT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=2000, state="visible")
                if el:
                    el.click()
                    el.fill(text)
                    break
            except Exception:
                continue

        StealthUtils.random_delay(500, 1000)

        # Submit
        print("  Submitting...")
        for selector in SUBMIT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=2000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    break
            except Exception:
                continue
        else:
            page.keyboard.press("Enter")

        StealthUtils.random_delay(3000, 5000)

        return {
            "status": "success",
            "source_type": "text",
            "title": title,
            "text_length": len(text),
            "notebook_url": notebook_url,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        if context:
            try:
                context.close()
            except Exception:
                pass
        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass


def add_file_source(notebook_url: str, file_path: str, headless: bool = True) -> dict:
    """Upload a file as a source to a notebook."""
    path = Path(file_path)
    if not path.exists():
        return {"status": "error", "message": f"File not found: {file_path}"}

    auth = AuthManager()
    if not auth.is_authenticated():
        return {"status": "error", "message": "Not authenticated"}

    print(f"Uploading file source: {path.name}")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        page = context.new_page()

        page.goto(notebook_url, wait_until="domcontentloaded")
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=15000)
        StealthUtils.random_delay(1500, 2500)

        # Try direct file input first (fastest path)
        print("  Looking for file input...")
        uploaded = False
        for selector in FILE_INPUT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000)
                if el:
                    el.set_input_files(str(path.resolve()))
                    uploaded = True
                    print("  File uploaded via input element")
                    break
            except Exception:
                continue

        if not uploaded:
            # Click "Add source" then "Upload"
            print("  Trying 'Add source' -> 'Upload' path...")
            for selector in ADD_SOURCE_SELECTORS:
                try:
                    el = page.wait_for_selector(selector, timeout=3000, state="visible")
                    if el:
                        StealthUtils.realistic_click(page, selector)
                        break
                except Exception:
                    continue

            StealthUtils.random_delay(1000, 1500)

            for selector in SOURCE_TYPE_FILE_SELECTORS:
                try:
                    el = page.wait_for_selector(selector, timeout=3000, state="visible")
                    if el:
                        if el.get_attribute("type") == "file":
                            el.set_input_files(str(path.resolve()))
                        else:
                            StealthUtils.realistic_click(page, selector)
                            StealthUtils.random_delay(500, 1000)
                            for fs in FILE_INPUT_SELECTORS:
                                try:
                                    fel = page.wait_for_selector(fs, timeout=3000)
                                    if fel:
                                        fel.set_input_files(str(path.resolve()))
                                        break
                                except Exception:
                                    continue
                        uploaded = True
                        break
                except Exception:
                    continue

        # Wait for upload processing
        print("  Waiting for file processing...")
        StealthUtils.random_delay(5000, 10000)

        return {
            "status": "success",
            "source_type": "file",
            "file_name": path.name,
            "file_size": path.stat().st_size,
            "notebook_url": notebook_url,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        if context:
            try:
                context.close()
            except Exception:
                pass
        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(description="Add source to NotebookLM notebook")
    parser.add_argument("--type", required=True, choices=["url", "text", "file"],
                        help="Source type: url, text, or file")
    parser.add_argument("--notebook-url", help="Notebook URL")
    parser.add_argument("--notebook-id", help="Notebook ID from library")

    # URL source args
    parser.add_argument("--url", help="URL to add as source")

    # Text source args
    parser.add_argument("--title", help="Title for text source")
    parser.add_argument("--text", help="Text content to add")

    # File source args
    parser.add_argument("--file", help="File path to upload")

    parser.add_argument("--show-browser", action="store_true", help="Show browser")

    args = parser.parse_args()

    notebook_url = _resolve_notebook_url(args.notebook_url, args.notebook_id)
    if not notebook_url:
        return 1

    headless = not args.show_browser

    if args.type == "url":
        if not args.url:
            print("--url is required for URL source type")
            return 1
        result = add_url_source(notebook_url, args.url, headless)

    elif args.type == "text":
        if not args.title or not args.text:
            print("--title and --text are required for text source type")
            return 1
        result = add_text_source(notebook_url, args.title, args.text, headless)

    elif args.type == "file":
        if not args.file:
            print("--file is required for file source type")
            return 1
        result = add_file_source(notebook_url, args.file, headless)

    print(f"\nResult: {result}")
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
