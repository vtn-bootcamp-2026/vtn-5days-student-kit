#!/usr/bin/env python3
"""
Create a new NotebookLM notebook via browser automation.
Navigates to NotebookLM homepage, creates a new notebook, and returns its URL.
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
from browser_utils import BrowserFactory, StealthUtils
from config import BROWSER_ARGS, USER_AGENT


# Selectors for NotebookLM UI elements
NOTEBOOKLM_HOME = "https://notebooklm.google.com/"

# "New notebook" / "Create" button selectors (multiple fallbacks)
NEW_NOTEBOOK_SELECTORS = [
    'button[aria-label*="New"]',
    'button[aria-label*="Create"]',
    'button[aria-label*="new notebook"]',
    'button[aria-label*="Tạo"]',
    'a[href*="create"]',
    '[data-test-id="create-notebook"]',
    '.new-notebook-button',
    'button.mat-mdc-fab',
    'button.create-button',
]

# Notebook title/name input selectors
TITLE_INPUT_SELECTORS = [
    'input[aria-label*="title"]',
    'input[aria-label*="name"]',
    'input[aria-label*="Title"]',
    'input[aria-label*="Name"]',
    'input[placeholder*="title"]',
    'input[placeholder*="name"]',
    'input[placeholder*="Enter"]',
    'input[data-test-id="notebook-title"]',
    '.notebook-title-input input',
]

# Confirm/create button after entering title
CONFIRM_SELECTORS = [
    'button[aria-label*="Create"]',
    'button[aria-label*="create"]',
    'button[aria-label*="Save"]',
    'button[aria-label*="Done"]',
    'button:has-text("Create")',
    'button:has-text("Create notebook")',
    'button:has-text("Done")',
]


def create_notebook(title: str, description: str = "", headless: bool = True) -> dict:
    """
    Create a new NotebookLM notebook.

    Args:
        title: Notebook title
        description: Optional description
        headless: Run browser in headless mode

    Returns:
        Dict with 'url', 'title', 'status'
    """
    auth = AuthManager()
    if not auth.is_authenticated():
        return {"status": "error", "message": "Not authenticated. Run auth_manager.py setup first."}

    print(f"📓 Creating notebook: {title}")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        page = context.new_page()

        # Navigate to NotebookLM homepage
        print("  Navigating to NotebookLM...")
        page.goto(NOTEBOOKLM_HOME, wait_until="domcontentloaded")
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com"), timeout=15000)
        StealthUtils.random_delay(1000, 2000)

        # Try to find and click "New notebook" button
        print("  Looking for 'New notebook' button...")
        clicked = False
        for selector in NEW_NOTEBOOK_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    clicked = True
                    print(f"  Clicked: {selector}")
                    break
            except Exception:
                continue

        if not clicked:
            # Try clicking by text content
            try:
                page.click('text=/New|Create|Tạo|Neu/i', timeout=3000)
                clicked = True
                print("  Clicked via text match")
            except Exception:
                pass

        if not clicked:
            # Try direct URL approach - some versions allow direct creation
            page.goto(f"{NOTEBOOKLM_HOME}create", wait_until="domcontentloaded")
            StealthUtils.random_delay(1000, 2000)

        StealthUtils.random_delay(1000, 2000)

        # Try to enter title
        print("  Entering notebook title...")
        title_entered = False
        for selector in TITLE_INPUT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    el.click()
                    el.fill(title)
                    title_entered = True
                    print(f"  Title entered via: {selector}")
                    break
            except Exception:
                continue

        if not title_entered:
            # Try active element approach - click whatever is focused
            try:
                page.keyboard.press("Tab")
                StealthUtils.random_delay(200, 500)
                page.keyboard.type(title, delay=50)
                title_entered = True
                print("  Title entered via keyboard")
            except Exception:
                pass

        StealthUtils.random_delay(500, 1000)

        # Try to enter description if provided
        if description:
            try:
                desc_selectors = [
                    'textarea[aria-label*="description"]',
                    'textarea[aria-label*="Description"]',
                    'textarea[placeholder*="description"]',
                    'textarea[placeholder*="Describe"]',
                ]
                for sel in desc_selectors:
                    try:
                        el = page.wait_for_selector(sel, timeout=2000, state="visible")
                        if el:
                            el.click()
                            el.fill(description)
                            break
                    except Exception:
                        continue
            except Exception:
                pass

        # Try to confirm/submit
        print("  Submitting...")
        confirmed = False
        for selector in CONFIRM_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=2000, state="visible")
                if el:
                    StealthUtils.realistic_click(page, selector)
                    confirmed = True
                    print(f"  Confirmed via: {selector}")
                    break
            except Exception:
                continue

        if not confirmed:
            page.keyboard.press("Enter")
            print("  Submitted via Enter key")

        # Wait for redirect to new notebook
        print("  Waiting for notebook creation...")
        try:
            page.wait_for_url(re.compile(r"https://notebooklm\.google\.com/notebook/"), timeout=15000)
            notebook_url = page.url
            print(f"  Notebook created: {notebook_url}")
            return {
                "status": "success",
                "url": notebook_url,
                "title": title,
            }
        except Exception:
            # Check if we're still on the same page but notebook was created
            current_url = page.url
            if "/notebook/" in current_url:
                return {
                    "status": "success",
                    "url": current_url,
                    "title": title,
                }
            else:
                return {
                    "status": "partial",
                    "url": current_url,
                    "title": title,
                    "message": "Notebook may have been created but URL confirmation failed. Check manually.",
                }

    except Exception as e:
        print(f"  Error: {e}")
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
    parser = argparse.ArgumentParser(description="Create a new NotebookLM notebook")
    parser.add_argument("--title", required=True, help="Notebook title")
    parser.add_argument("--description", default="", help="Notebook description")
    parser.add_argument("--show-browser", action="store_true", help="Show browser window")
    args = parser.parse_args()

    result = create_notebook(
        title=args.title,
        description=args.description,
        headless=not args.show_browser,
    )

    print(f"\nResult: {result}")
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
