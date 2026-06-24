#!/usr/bin/env python3
"""
Create NotebookLM artifacts via browser automation.
Supports: Audio Overview (podcast), and other artifact types.
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


# Artifact type selectors
ARTIFACT_SELECTORS = {
    "podcast": {
        "trigger": [
            'button[aria-label*="Audio overview"]',
            'button[aria-label*="Audio Overview"]',
            'button[aria-label*="podcast"]',
            'button[aria-label*="Deep dive"]',
            'button[aria-label*="Generate audio"]',
            '[data-test-id="audio-overview"]',
            'button:has-text("Audio overview")',
            'button:has-text("Generate")',
        ],
        "generate": [
            'button[aria-label*="Generate"]',
            'button[aria-label*="Create"]',
            'button:has-text("Generate")',
            'button:has-text("Create")',
        ],
    },
    "faq": {
        "trigger": [
            'button[aria-label*="FAQ"]',
            'button[aria-label*="Frequently asked"]',
            'button:has-text("FAQ")',
            'button:has-text("Frequently asked")',
            '[data-test-id="faq"]',
        ],
        "generate": [
            'button[aria-label*="Generate"]',
            'button:has-text("Generate")',
        ],
    },
    "study_guide": {
        "trigger": [
            'button[aria-label*="Study guide"]',
            'button[aria-label*="Study Guide"]',
            'button:has-text("Study guide")',
            '[data-test-id="study-guide"]',
        ],
        "generate": [
            'button[aria-label*="Generate"]',
            'button:has-text("Generate")',
        ],
    },
    "briefing_doc": {
        "trigger": [
            'button[aria-label*="Briefing"]',
            'button[aria-label*="briefing doc"]',
            'button:has-text("Briefing")',
            '[data-test-id="briefing-doc"]',
        ],
        "generate": [
            'button[aria-label*="Generate"]',
            'button:has-text("Generate")',
        ],
    },
}

# Notebook guide / studio panel selectors
NOTEBOOK_GUIDE_SELECTORS = [
    'button[aria-label*="Notebook guide"]',
    'button[aria-label*="Studio"]',
    'button[aria-label*="studio"]',
    'button:has-text("Notebook guide")',
    'button:has-text("Studio")',
    '[data-test-id="notebook-guide"]',
    '[data-test-id="studio"]',
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


def create_artifact(
    notebook_url: str,
    artifact_type: str,
    instructions: str = "",
    headless: bool = True,
) -> dict:
    """
    Create an artifact in a NotebookLM notebook.

    Args:
        notebook_url: URL of the notebook
        artifact_type: Type of artifact (podcast, faq, study_guide, briefing_doc)
        instructions: Optional custom instructions for generation
        headless: Run browser in headless mode

    Returns:
        Dict with status and details
    """
    auth = AuthManager()
    if not auth.is_authenticated():
        return {"status": "error", "message": "Not authenticated"}

    if artifact_type not in ARTIFACT_SELECTORS:
        return {
            "status": "error",
            "message": f"Unknown artifact type: {artifact_type}. Supported: {list(ARTIFACT_SELECTORS.keys())}",
        }

    print(f"Creating artifact: {artifact_type}")
    print(f"  Notebook: {notebook_url}")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        page = context.new_page()

        # Navigate to notebook
        print("  Navigating to notebook...")
        page.goto(notebook_url, wait_until="domcontentloaded")
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=15000)
        StealthUtils.random_delay(2000, 3000)

        # First, try to open Notebook Guide / Studio panel
        print("  Opening Notebook Guide / Studio...")
        guide_opened = _click_first_match(page, NOTEBOOK_GUIDE_SELECTORS, timeout=3000)
        if guide_opened:
            print("  Opened guide panel")
            StealthUtils.random_delay(1000, 2000)

        # Click the artifact type trigger
        selectors = ARTIFACT_SELECTORS[artifact_type]
        print(f"  Looking for {artifact_type} trigger...")
        triggered = _click_first_match(page, selectors["trigger"], timeout=5000)

        if not triggered:
            # Try text-based click
            try:
                page.click(f'text=/{artifact_type.replace("_", " ")}/i', timeout=3000)
                triggered = True
            except Exception:
                pass

        if not triggered:
            # For podcast, try the most common path: look for audio-related elements
            if artifact_type == "podcast":
                try:
                    page.click('text=/Audio|Podcast|Deep dive|Overview/i', timeout=3000)
                    triggered = True
                except Exception:
                    pass

        if not triggered:
            return {
                "status": "error",
                "message": f"Could not find {artifact_type} trigger element. The UI may have changed.",
            }

        print(f"  Triggered {artifact_type}")
        StealthUtils.random_delay(1000, 2000)

        # Enter custom instructions if provided
        if instructions:
            print("  Entering custom instructions...")
            instruction_selectors = [
                'textarea[aria-label*="instruction"]',
                'textarea[aria-label*="Instruction"]',
                'textarea[aria-label*="custom"]',
                'textarea[aria-label*="Customize"]',
                'textarea[placeholder*="instruction"]',
                'textarea[placeholder*="customize"]',
                'textarea[placeholder*="Describe"]',
            ]
            for selector in instruction_selectors:
                try:
                    el = page.wait_for_selector(selector, timeout=2000, state="visible")
                    if el:
                        el.click()
                        el.fill(instructions)
                        print("  Instructions entered")
                        break
                except Exception:
                    continue
            StealthUtils.random_delay(500, 1000)

        # Click Generate
        print("  Clicking Generate...")
        generated = _click_first_match(page, selectors["generate"], timeout=3000)

        if not generated:
            try:
                page.click('text=/Generate|Create|Start/i', timeout=3000)
                generated = True
            except Exception:
                pass

        if not generated:
            return {
                "status": "error",
                "message": "Could not find Generate button",
            }

        print("  Generation started!")

        # Wait for generation to complete (artifact types vary in time)
        # Podcast can take 2-5 minutes, others are faster
        timeout_seconds = 300 if artifact_type == "podcast" else 120
        print(f"  Waiting for generation (up to {timeout_seconds}s)...")

        # Poll for completion indicators
        deadline = time.time() + timeout_seconds
        completed = False
        last_status = ""

        while time.time() < deadline:
            try:
                # Check for progress/loading indicators
                loading_selectors = [
                    '.progress-bar',
                    '[aria-busy="true"]',
                    'div.loading',
                    'div.generating',
                    '.mat-progress-bar',
                ]
                is_loading = False
                for sel in loading_selectors:
                    try:
                        el = page.query_selector(sel)
                        if el and el.is_visible():
                            is_loading = True
                            break
                    except Exception:
                        continue

                # Check for completion indicators
                completion_selectors = [
                    'button[aria-label*="Play"]',
                    'button[aria-label*="Download"]',
                    'button:has-text("Play")',
                    'button:has-text("Download")',
                    'audio source',
                    'audio',
                    '.artifact-complete',
                ]
                for sel in completion_selectors:
                    try:
                        el = page.query_selector(sel)
                        if el and el.is_visible():
                            completed = True
                            break
                    except Exception:
                        continue

                if completed:
                    break

                # Report progress
                current_status = "generating" if is_loading else "waiting"
                if current_status != last_status:
                    elapsed = int(time.time() - (deadline - timeout_seconds))
                    print(f"  Status: {current_status} ({elapsed}s elapsed)")
                    last_status = current_status

                time.sleep(3)

            except Exception:
                time.sleep(3)
                continue

        if completed:
            print("  Artifact generated successfully!")
            return {
                "status": "success",
                "artifact_type": artifact_type,
                "notebook_url": notebook_url,
                "message": f"{artifact_type} artifact created successfully. Check the notebook to view/download.",
            }
        else:
            print("  Generation may still be in progress (timeout reached)")
            return {
                "status": "timeout",
                "artifact_type": artifact_type,
                "notebook_url": notebook_url,
                "message": f"Generation started but did not complete within {timeout_seconds}s. Check notebook manually.",
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


def list_artifact_types():
    """Return supported artifact types."""
    return list(ARTIFACT_SELECTORS.keys())


def main():
    parser = argparse.ArgumentParser(description="Create NotebookLM artifact")
    parser.add_argument(
        "--type",
        required=True,
        choices=list(ARTIFACT_SELECTORS.keys()),
        help="Artifact type to create",
    )
    parser.add_argument("--notebook-url", help="Notebook URL")
    parser.add_argument("--notebook-id", help="Notebook ID from library")
    parser.add_argument("--instructions", default="", help="Custom instructions")
    parser.add_argument("--show-browser", action="store_true", help="Show browser")

    args = parser.parse_args()

    notebook_url = _resolve_notebook_url(args.notebook_url, args.notebook_id)
    if not notebook_url:
        return 1

    result = create_artifact(
        notebook_url=notebook_url,
        artifact_type=args.type,
        instructions=args.instructions,
        headless=not args.show_browser,
    )

    print(f"\nResult: {result}")
    return 0 if result["status"] in ("success", "timeout") else 1


if __name__ == "__main__":
    sys.exit(main())
