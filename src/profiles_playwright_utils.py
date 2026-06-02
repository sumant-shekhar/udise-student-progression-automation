"""
Playwright utilities for profile automation with retry logic and stale element handling.
Replaces Selenium WebDriverUtils with Playwright equivalents.
"""

import time
from typing import Optional, Callable
from playwright.sync_api import Page, ElementHandle, TimeoutError as PlaywrightTimeoutError


class ProfilePlaywrightUtils:
    """Utility wrapper for resilient Playwright element interactions."""

    def __init__(self, page: Page, wait_timeout: int = 20000):
        """
        Initialize Playwright utilities.

        Args:
            page: Playwright page object
            wait_timeout: Default timeout in milliseconds
        """
        self.page = page
        self.wait_timeout = wait_timeout

    def safe_js(self, xpath: str, script: str, retries: int = 3) -> ElementHandle:
        """
        Execute JavaScript on element with retry logic.

        Args:
            xpath: XPath selector
            script: JavaScript code to execute
            retries: Number of retry attempts

        Returns:
            Element handle

        Raises:
            Exception: If element not found after retries
        """
        for attempt in range(retries):
            try:
                el = self.page.locator(f"xpath={xpath}").first
                el.wait_for(state="attached", timeout=self.wait_timeout)
                self.page.evaluate(f"(el) => {script}", el)
                return el
            except PlaywrightTimeoutError:
                if attempt < retries - 1:
                    print(f"  ⚠️ Element not found, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.3)
                else:
                    raise Exception(f"safe_js: Element not found within timeout: {xpath}")
            except Exception as e:
                if attempt < retries - 1:
                    print(f"  ⚠️ Error executing script, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.3)
                else:
                    raise

    def safe_input(self, xpath: str, value: str, retries: int = 3) -> ElementHandle:
        """
        Fill input field with retry logic.

        Args:
            xpath: XPath selector
            value: Value to input
            retries: Number of retry attempts

        Returns:
            Element handle

        Raises:
            Exception: If element not found after retries
        """
        for attempt in range(retries):
            try:
                el = self.page.locator(f"xpath={xpath}").first
                el.wait_for(state="attached", timeout=self.wait_timeout)
                el.clear()
                el.fill(value)
                return el
            except PlaywrightTimeoutError:
                if attempt < retries - 1:
                    print(f"  ⚠️ Input not found, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.3)
                else:
                    raise Exception(f"safe_input: Input not found within timeout: {xpath}")
            except Exception as e:
                if attempt < retries - 1:
                    print(f"  ⚠️ Error filling input, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.3)
                else:
                    raise

    def dispatch_change(self, xpath: str) -> None:
        """
        Dispatch change event on element.

        Args:
            xpath: XPath selector
        """
        self.safe_js(xpath, "arguments[0].dispatchEvent(new Event('change'))")
        time.sleep(0.15)

    def js_click(self, xpath: str, retries: int = 3) -> ElementHandle:
        """
        Click element using JavaScript with retry logic.

        Args:
            xpath: XPath selector
            retries: Number of retry attempts

        Returns:
            Element handle

        Raises:
            Exception: If element not clickable after retries
        """
        for attempt in range(retries):
            try:
                el = self.page.locator(f"xpath={xpath}").first
                el.wait_for(state="attached", timeout=self.wait_timeout)
                self.page.evaluate("(el) => el.click();", el)
                return el
            except PlaywrightTimeoutError:
                if attempt < retries - 1:
                    print(f"  ⚠️ Element not found on click, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.2)
                else:
                    raise Exception(f"js_click: Element not found within timeout: {xpath}")
            except Exception as e:
                if attempt < retries - 1:
                    print(f"  ⚠️ Error on click, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.2)
                else:
                    raise

    def js_click_css(self, css: str, retries: int = 3) -> ElementHandle:
        """
        Click element by CSS selector using JavaScript with retry logic.

        Args:
            css: CSS selector
            retries: Number of retry attempts

        Returns:
            Element handle

        Raises:
            Exception: If element not clickable after retries
        """
        for attempt in range(retries):
            try:
                el = self.page.locator(css).first
                el.wait_for(state="attached", timeout=self.wait_timeout)
                self.page.evaluate("(el) => el.click();", el)
                return el
            except PlaywrightTimeoutError:
                if attempt < retries - 1:
                    print(f"  ⚠️ Element not found on CSS click, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.2)
                else:
                    raise Exception(f"js_click_css: Element not found within timeout: {css}")
            except Exception as e:
                if attempt < retries - 1:
                    print(f"  ⚠️ Error on CSS click, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.2)
                else:
                    raise

    def get_attribute(self, xpath: str, attr: str, default: str = "") -> str:
        """
        Get element attribute value.

        Args:
            xpath: XPath selector
            attr: Attribute name
            default: Default value if attribute not found

        Returns:
            Attribute value
        """
        try:
            el = self.page.locator(f"xpath={xpath}").first
            el.wait_for(state="attached", timeout=self.wait_timeout)
            value = el.get_attribute(attr)
            return value or default
        except Exception:
            return default

    def get_input_value(self, xpath: str) -> str:
        """
        Get value from input field.

        Args:
            xpath: XPath selector

        Returns:
            Input value
        """
        try:
            el = self.page.locator(f"xpath={xpath}").first
            el.wait_for(state="attached", timeout=self.wait_timeout)
            value = el.input_value()
            return value.strip() if value else ""
        except Exception:
            return ""

    def get_selected_option_value(self, css: str) -> str:
        """
        Get selected option value from dropdown.

        Args:
            css: CSS selector for select element

        Returns:
            Selected option value
        """
        try:
            el = self.page.locator(css).first
            el.wait_for(state="attached", timeout=self.wait_timeout)
            value = el.locator("option:checked").first.get_attribute("value")
            return value or ""
        except Exception:
            return ""

    def get_selected_option_text(self, css: str) -> str:
        """
        Get selected option text from dropdown.

        Args:
            css: CSS selector for select element

        Returns:
            Selected option text
        """
        try:
            el = self.page.locator(css).first
            el.wait_for(state="attached", timeout=self.wait_timeout)
            text = el.locator("option:checked").first.text_content()
            return text.strip() if text else ""
        except Exception:
            return ""

    def select_by_value(self, css: str, value: str, retries: int = 3) -> None:
        """
        Select option by value in dropdown.

        Args:
            css: CSS selector for select element
            value: Option value
            retries: Number of retry attempts
        """
        for attempt in range(retries):
            try:
                el = self.page.locator(css).first
                el.wait_for(state="attached", timeout=self.wait_timeout)
                el.select_option(value=value)
                return
            except Exception as e:
                if attempt < retries - 1:
                    print(f"  ⚠️ Error selecting option, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.3)
                else:
                    raise

    def select_by_text(self, css: str, text: str, retries: int = 3) -> None:
        """
        Select option by visible text in dropdown.

        Args:
            css: CSS selector for select element
            text: Option text
            retries: Number of retry attempts
        """
        for attempt in range(retries):
            try:
                el = self.page.locator(css).first
                el.wait_for(state="attached", timeout=self.wait_timeout)
                el.select_option(label=text)
                return
            except Exception as e:
                if attempt < retries - 1:
                    print(f"  ⚠️ Error selecting option by text, retrying ({attempt + 1}/{retries})...")
                    time.sleep(0.3)
                else:
                    raise

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.2)

    def wait_for_element(self, xpath: str, timeout: Optional[int] = None) -> ElementHandle:
        """
        Wait for element to be present.

        Args:
            xpath: XPath selector
            timeout: Timeout in milliseconds (uses default if None)

        Returns:
            Element handle
        """
        timeout = timeout or self.wait_timeout
        el = self.page.locator(f"xpath={xpath}").first
        el.wait_for(state="attached", timeout=timeout)
        return el

    def element_exists(self, xpath: str) -> bool:
        """
        Check if element exists.

        Args:
            xpath: XPath selector

        Returns:
            True if element exists, False otherwise
        """
        try:
            count = self.page.locator(f"xpath={xpath}").count()
            return count > 0
        except Exception:
            return False
