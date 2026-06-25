#!/usr/bin/env python3
"""
Simple NotebookLM Question Interface
Based on MCP server implementation - simplified without sessions

Implements hybrid auth approach:
- Persistent browser profile (user_data_dir) for fingerprint consistency
- Manual cookie injection from state.json for session cookies (Playwright bug workaround)
See: https://github.com/microsoft/playwright/issues/36139
"""

import argparse
import sys
import time
import re
from pathlib import Path

from patchright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from notebook_manager import NotebookLibrary
from config import QUERY_INPUT_SELECTORS, RESPONSE_SELECTORS
from browser_utils import BrowserFactory, StealthUtils


# Follow-up reminder (adapted from MCP server for stateless operation)
# Since we don't have persistent sessions, we encourage comprehensive questions
FOLLOW_UP_REMINDER = (
    "\n\nEXTREMELY IMPORTANT: Is that ALL you need to know? "
    "You can always ask another question! Think about it carefully: "
    "before you reply to the user, review their original request and this answer. "
    "If anything is still unclear or missing, ask me another comprehensive question "
    "that includes all necessary context (since each question opens a new browser session)."
)


def _response_state(page):
    """Return the largest response count and its latest text across known selectors."""
    best_count = 0
    latest_text = None

    for selector in RESPONSE_SELECTORS:
        try:
            elements = page.query_selector_all(selector)
            if len(elements) > best_count:
                best_count = len(elements)
                latest_text = elements[-1].inner_text().strip() if elements else None
        except:
            continue

    return best_count, latest_text


def _wait_for_history_to_settle(page, timeout_seconds: int = 8):
    """NotebookLM can lazy-render previous chat answers after page load."""
    deadline = time.time() + timeout_seconds
    last_count = -1
    stable_count = 0
    latest_text = None

    while time.time() < deadline:
        count, text = _response_state(page)
        if count == last_count:
            stable_count += 1
            if stable_count >= 2:
                return count, text
        else:
            stable_count = 0
            last_count = count
            latest_text = text
        time.sleep(1)

    return last_count if last_count >= 0 else 0, latest_text


def _extract_answer_after_question(page, question: str):
    """Fallback for NotebookLM UI variants where response selectors point to older answers."""
    try:
        body_text = page.locator("body").inner_text(timeout=5000)
    except:
        return None

    if question not in body_text:
        return None

    tail = body_text.rsplit(question, 1)[-1].strip()
    if not tail:
        return None

    thinking_markers = [
        "Đang suy nghĩ",
        "Assessing relevance",
        "Getting the gist",
        "Analyzing the Requirements",
    ]
    if any(marker in tail for marker in thinking_markers):
        return None

    end_markers = [
        "\nkeep_pin",
        "\nHướng dẫn",
        "\nNotebookLM có thể đưa ra",
        "\ncopy_all",
        "\nthumb_up",
    ]
    answer = tail
    for marker in end_markers:
        if marker in answer:
            answer = answer.split(marker, 1)[0]

    answer = answer.strip()
    if len(answer) < 20:
        return None
    return answer


def ask_notebooklm(question: str, notebook_url: str, headless: bool = True) -> str:
    """
    Ask a question to NotebookLM

    Args:
        question: Question to ask
        notebook_url: NotebookLM notebook URL
        headless: Run browser in headless mode

    Returns:
        Answer text from NotebookLM
    """
    auth = AuthManager()

    if not auth.is_authenticated():
        print("⚠️ Not authenticated. Run: python auth_manager.py setup")
        return None

    print(f"💬 Asking: {question}")
    print(f"📚 Notebook: {notebook_url}")

    playwright = None
    context = None

    try:
        # Start playwright
        playwright = sync_playwright().start()

        # Launch persistent browser context using factory
        context = BrowserFactory.launch_persistent_context(
            playwright,
            headless=headless
        )

        # Navigate to notebook
        page = context.new_page()
        print("  🌐 Opening notebook...")
        page.goto(notebook_url, wait_until="domcontentloaded")

        # Wait for NotebookLM
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=10000)

        # Wait for query input (MCP approach)
        print("  ⏳ Waiting for query input...")
        query_element = None

        for selector in QUERY_INPUT_SELECTORS:
            try:
                query_element = page.wait_for_selector(
                    selector,
                    timeout=10000,
                    state="visible"  # Only check visibility, not disabled!
                )
                if query_element:
                    print(f"  ✓ Found input: {selector}")
                    break
            except:
                continue

        if not query_element:
            print("  ❌ Could not find query input")
            return None

        # Capture current responses before submitting. NotebookLM keeps chat history
        # in the notebook, so accepting the last visible response immediately can
        # accidentally return an answer from a previous run.
        baseline_response_count, baseline_latest_text = _wait_for_history_to_settle(page)

        # Type question (human-like, fast)
        print("  ⏳ Typing question...")
        
        # Use primary selector for typing
        input_selector = QUERY_INPUT_SELECTORS[0]
        StealthUtils.human_type(page, input_selector, question)

        # Submit
        print("  📤 Submitting...")
        send_button = None
        for selector in [
            'button[aria-label="Gửi"]',
            'button[aria-label="Send"]',
            'button:has-text("arrow_forward")',
        ]:
            try:
                candidate = page.locator(selector).first
                if candidate and candidate.is_visible() and candidate.is_enabled():
                    send_button = candidate
                    break
            except:
                continue

        if send_button:
            send_button.click()
        else:
            page.keyboard.press("Enter")

        # Small pause
        StealthUtils.random_delay(500, 1500)

        # Wait for response (MCP approach: poll for stable text)
        print("  ⏳ Waiting for answer...")

        answer = None
        stable_count = 0
        last_text = None
        deadline = time.time() + 120  # 2 minutes timeout

        while time.time() < deadline:
            # Check if NotebookLM is still thinking (most reliable indicator)
            try:
                thinking_element = page.query_selector('div.thinking-message')
                if thinking_element and thinking_element.is_visible():
                    time.sleep(1)
                    continue
            except:
                pass

            extracted_answer = _extract_answer_after_question(page, question)
            if extracted_answer:
                answer = extracted_answer
                break

            # Try to find response with MCP selectors
            for selector in RESPONSE_SELECTORS:
                try:
                    elements = page.query_selector_all(selector)
                    if len(elements) > baseline_response_count:
                        # Get last (newest) response
                        latest = elements[-1]
                        text = latest.inner_text().strip()

                        if text:
                            if text == last_text:
                                stable_count += 1
                                if stable_count >= 3:  # Stable for 3 polls
                                    answer = text
                                    break
                            else:
                                stable_count = 0
                                last_text = text
                    elif elements and baseline_latest_text:
                        latest_text = elements[-1].inner_text().strip()
                        if latest_text and latest_text != baseline_latest_text:
                            if latest_text == last_text:
                                stable_count += 1
                                if stable_count >= 3:
                                    answer = latest_text
                                    break
                            else:
                                stable_count = 0
                                last_text = latest_text
                except:
                    continue

            if answer:
                break

            time.sleep(1)

        if not answer:
            print("  ❌ Timeout waiting for answer")
            return None

        print("  ✅ Got answer!")
        # Add follow-up reminder to encourage Claude to ask more questions
        return answer + FOLLOW_UP_REMINDER

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        # Always clean up
        if context:
            try:
                context.close()
            except:
                pass

        if playwright:
            try:
                playwright.stop()
            except:
                pass


def main():
    parser = argparse.ArgumentParser(description='Ask NotebookLM a question')

    parser.add_argument('--question', required=True, help='Question to ask')
    parser.add_argument('--notebook-url', help='NotebookLM notebook URL')
    parser.add_argument('--notebook-id', help='Notebook ID from library')
    parser.add_argument('--show-browser', action='store_true', help='Show browser')

    args = parser.parse_args()

    # Resolve notebook URL
    notebook_url = args.notebook_url

    if not notebook_url and args.notebook_id:
        library = NotebookLibrary()
        notebook = library.get_notebook(args.notebook_id)
        if notebook:
            notebook_url = notebook['url']
        else:
            print(f"❌ Notebook '{args.notebook_id}' not found")
            return 1

    if not notebook_url:
        # Check for active notebook first
        library = NotebookLibrary()
        active = library.get_active_notebook()
        if active:
            notebook_url = active['url']
            print(f"📚 Using active notebook: {active['name']}")
        else:
            # Show available notebooks
            notebooks = library.list_notebooks()
            if notebooks:
                print("\n📚 Available notebooks:")
                for nb in notebooks:
                    mark = " [ACTIVE]" if nb.get('id') == library.active_notebook_id else ""
                    print(f"  {nb['id']}: {nb['name']}{mark}")
                print("\nSpecify with --notebook-id or set active:")
                print("python scripts/run.py notebook_manager.py activate --id ID")
            else:
                print("❌ No notebooks in library. Add one first:")
                print("python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS")
            return 1

    # Ask the question
    answer = ask_notebooklm(
        question=args.question,
        notebook_url=notebook_url,
        headless=not args.show_browser
    )

    if answer:
        print("\n" + "=" * 60)
        print(f"Question: {args.question}")
        print("=" * 60)
        print()
        print(answer)
        print()
        print("=" * 60)
        return 0
    else:
        print("\n❌ Failed to get answer")
        return 1


if __name__ == "__main__":
    sys.exit(main())
