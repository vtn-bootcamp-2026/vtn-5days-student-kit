#!/usr/bin/env python3
"""
Update NotebookLM notebook settings via browser automation.
Supports: system prompt / notebook instructions update.
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


# Notebook guide / settings selectors
GUIDE_SELECTORS = [
    'button[aria-label*="Notebook guide"]',
    'button[aria-label*="notebook guide"]',
    'button[aria-label*="Settings"]',
    'button[aria-label*="Customize"]',
    'button:has-text("Notebook guide")',
    'button:has-text("Guide")',
    '[data-test-id="notebook-guide"]',
]

# System prompt / instructions textarea selectors
SYSTEM_PROMPT_SELECTORS = [
    'textarea[aria-label*="system"]',
    'textarea[aria-label*="System"]',
    'textarea[aria-label*="instruction"]',
    'textarea[aria-label*="Instruction"]',
    'textarea[aria-label*="prompt"]',
    'textarea[aria-label*="Prompt"]',
    'textarea[aria-label*="custom instruction"]',
    'textarea[aria-label*="Customize"]',
    'textarea[aria-label*="guide"]',
    'textarea[placeholder*="instruction"]',
    'textarea[placeholder*="system"]',
    'textarea[placeholder*="custom"]',
    'textarea[placeholder*="guide"]',
    'textarea[placeholder*="How should"]',
    '[data-test-id="system-prompt"] textarea',
    '[data-test-id="instructions"] textarea',
    '.system-prompt-textarea',
    '.instructions-textarea',
]

# Edit button for system prompt
EDIT_SELECTORS = [
    'button[aria-label*="Edit"]',
    'button[aria-label*="edit"]',
    'button[aria-label*="Modify"]',
    'button:has-text("Edit")',
    'button:has-text("Modify")',
    '[data-test-id="edit-instructions"]',
]

# Save button after editing
SAVE_SELECTORS = [
    'button[aria-label*="Save"]',
    'button[aria-label*="save"]',
    'button[aria-label*="Apply"]',
    'button:has-text("Save")',
    'button:has-text("Apply")',
    'button:has-text("Done")',
    '[data-test-id="save-instructions"]',
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


def _click_first_match(page, selectors, timeout=3000):
    """Try clicking each selector, return True if any succeeded."""
    for selector in selectors:
        try:
            el = page.wait_for_selector(selector, timeout=timeout, state="visible")
            if el:
                StealthUtils.realistic_click(page, selector)
                return True
        except Exception:
            continue
    return False


def get_system_prompt(notebook_url: str, headless: bool = True) -> dict:
    """
    Read the current system prompt / instructions from a notebook.

    Returns:
        Dict with 'status' and 'prompt' (current system prompt text)
    """
    auth = AuthManager()
    if not auth.is_authenticated():
        return {"status": "error", "message": "Not authenticated"}

    print("Reading system prompt...")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        page = context.new_page()

        page.goto(notebook_url, wait_until="domcontentloaded")
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=15000)
        StealthUtils.random_delay(2000, 3000)

        # Open Notebook Guide
        _click_first_match(page, GUIDE_SELECTORS, timeout=5000)
        StealthUtils.random_delay(1000, 2000)

        # Try to find and read the system prompt
        for selector in SYSTEM_PROMPT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    text = el.input_value() if el.get_attribute("contenteditable") is None else el.inner_text()
                    return {
                        "status": "success",
                        "prompt": text,
                    }
            except Exception:
                continue

        return {"status": "error", "message": "Could not find system prompt textarea"}

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


def update_system_prompt(notebook_url: str, prompt: str, headless: bool = True) -> dict:
    """
    Update the system prompt / instructions of a notebook.

    Args:
        notebook_url: URL of the notebook
        prompt: New system prompt text
        headless: Run browser in headless mode

    Returns:
        Dict with status
    """
    auth = AuthManager()
    if not auth.is_authenticated():
        return {"status": "error", "message": "Not authenticated"}

    print(f"Updating system prompt ({len(prompt)} chars)...")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        page = context.new_page()

        page.goto(notebook_url, wait_until="domcontentloaded")
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=15000)
        StealthUtils.random_delay(2000, 3000)

        # Open Notebook Guide
        print("  Opening Notebook Guide...")
        guide_opened = _click_first_match(page, GUIDE_SELECTORS, timeout=5000)
        if not guide_opened:
            try:
                page.click('text=/Guide|Settings|Customize/i', timeout=3000)
                guide_opened = True
            except Exception:
                pass

        if not guide_opened:
            return {"status": "error", "message": "Could not open Notebook Guide"}

        StealthUtils.random_delay(1000, 2000)

        # Try to click Edit button first
        print("  Looking for Edit button...")
        _click_first_match(page, EDIT_SELECTORS, timeout=3000)
        StealthUtils.random_delay(500, 1000)

        # Find and update the system prompt textarea
        print("  Looking for system prompt textarea...")
        prompt_updated = False
        for selector in SYSTEM_PROMPT_SELECTORS:
            try:
                el = page.wait_for_selector(selector, timeout=3000, state="visible")
                if el:
                    # Clear existing content
                    el.click()
                    page.keyboard.press("Meta+A")
                    page.keyboard.press("Backspace")
                    StealthUtils.random_delay(200, 400)

                    # Enter new prompt
                    el.fill(prompt)
                    prompt_updated = True
                    print(f"  Prompt updated via: {selector}")
                    break
            except Exception:
                continue

        if not prompt_updated:
            return {"status": "error", "message": "Could not find system prompt textarea"}

        StealthUtils.random_delay(500, 1000)

        # Save
        print("  Saving...")
        saved = _click_first_match(page, SAVE_SELECTORS, timeout=3000)

        if not saved:
            try:
                page.click('text=/Save|Apply|Done/i', timeout=3000)
                saved = True
            except Exception:
                pass

        if not saved:
            # Try keyboard shortcut
            page.keyboard.press("Meta+Enter")
            StealthUtils.random_delay(500, 1000)

        print("  System prompt updated!")
        return {
            "status": "success",
            "prompt_length": len(prompt),
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
    parser = argparse.ArgumentParser(description="Update NotebookLM notebook settings")
    parser.add_argument("--notebook-url", help="Notebook URL")
    parser.add_argument("--notebook-id", help="Notebook ID from library")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Get prompt
    subparsers.add_parser("get", help="Get current system prompt")

    # Set prompt
    set_parser = subparsers.add_parser("set", help="Set system prompt")
    set_parser.add_argument("--prompt", required=True, help="New system prompt text")
    set_parser.add_argument("--file", help="Read prompt from file")

    parser.add_argument("--show-browser", action="store_true", help="Show browser")

    args = parser.parse_args()

    notebook_url = _resolve_notebook_url(args.notebook_url, args.notebook_id)
    if not notebook_url:
        return 1

    headless = not args.show_browser

    if args.command == "get":
        result = get_system_prompt(notebook_url, headless)
    elif args.command == "set":
        prompt_text = args.prompt
        if args.file:
            prompt_text = Path(args.file).read_text()
        result = update_system_prompt(notebook_url, prompt_text, headless)
    else:
        parser.print_help()
        return 1

    print(f"\nResult: {result}")
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
