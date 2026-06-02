"""
Playwright utility wrapper for UDISE+ automation workflows
Provides resilient element interaction and navigation helpers
"""

from typing import List, Optional, Any, Callable
import time
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError


class PlaywrightUtils:
    """Utility class for reliable Playwright interactions with automatic retries and waits"""

    def __init__(self, page: Page, base_timeout: int = 5000):
        """
        Initialize Playwright utilities.
        
        Args:
            page: Playwright Page instance
            base_timeout: Default timeout in milliseconds for element interactions
        """
        self.page = page
        self.base_timeout = base_timeout

    def xpath(self, path: str) -> str:
        """Convert XPath to Playwright selector format"""
        return f"xpath={path}"

    def wait_for_element(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> Locator:
        """
        Wait for an element to reach a specific state.
        
        Args:
            selector: CSS/XPath selector
            state: "visible", "attached", "hidden", "disabled"
            timeout: Custom timeout in ms; uses base_timeout if None
            
        Returns:
            Locator object
        """
        timeout = timeout or self.base_timeout
        locator = self.page.locator(selector)
        try:
            locator.wait_for(state=state, timeout=timeout)
            return locator
        except PlaywrightTimeoutError as e:
            raise TimeoutError(f"Element not {state} within {timeout}ms: {selector}") from e

    def safe_input(self, selector: str, value: str, clear_first: bool = True, timeout: Optional[int] = None) -> bool:
        """
        Safely fill an input field with robust error handling.
        
        Args:
            selector: CSS/XPath selector
            value: Value to input
            clear_first: Clear field before typing
            timeout: Custom timeout in ms
            
        Returns:
            True if successful, False otherwise
        """
        try:
            timeout = timeout or self.base_timeout
            locator = self.wait_for_element(selector, "visible", timeout)
            
            if clear_first:
                locator.fill("")
            
            locator.type(value, delay=10)  # slight delay between keystrokes for stability
            return True
        except Exception as e:
            print(f"❌ safe_input failed for {selector}: {e}")
            return False

    def safe_click(self, selector: str, timeout: Optional[int] = None, max_retries: int = 3) -> bool:
        """
        Safely click an element with automatic retry logic.
        
        Args:
            selector: CSS/XPath selector
            timeout: Custom timeout in ms
            max_retries: Number of retry attempts
            
        Returns:
            True if successful, False otherwise
        """
        timeout = timeout or self.base_timeout
        
        for attempt in range(max_retries):
            try:
                locator = self.wait_for_element(selector, "visible", timeout)
                locator.click()
                return True
            except PlaywrightTimeoutError as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Click timeout (attempt {attempt + 1}/{max_retries}), retrying...")
                    time.sleep(0.3)
                else:
                    print(f"❌ Click failed after {max_retries} attempts: {selector}")
                    return False
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Click error (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(0.3)
                else:
                    print(f"❌ Click error after {max_retries} attempts: {e}")
                    return False
        
        return False

    def safe_select(self, selector: str, value: str, timeout: Optional[int] = None) -> bool:
        """
        Safely select an option from a dropdown.
        
        Args:
            selector: CSS/XPath selector
            value: Option value to select
            timeout: Custom timeout in ms
            
        Returns:
            True if successful, False otherwise
        """
        try:
            timeout = timeout or self.base_timeout
            locator = self.wait_for_element(selector, "attached", timeout)
            
            # Try native select first
            try:
                locator.select_option(value)
                return True
            except Exception:
                # Fallback to JS manipulation if select_option fails
                self.page.evaluate(
                    f"""(sel, val) => {{
                        const el = document.evaluate('{selector.replace("xpath=", "")}', 
                            document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (el) {{
                            el.value = val;
                            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    }}""",
                    value
                )
                return True
        except Exception as e:
            print(f"❌ safe_select failed for {selector}: {e}")
            return False

    def get_select_options(self, selector: str, timeout: Optional[int] = None) -> List[str]:
        """
        Get all available options from a dropdown.
        
        Args:
            selector: CSS/XPath selector for select element
            timeout: Custom timeout in ms
            
        Returns:
            List of option values
        """
        try:
            timeout = timeout or self.base_timeout
            self.wait_for_element(selector, "attached", timeout)
            
            # Extract via JS for XPath compatibility
            options = self.page.evaluate(
                f"""() => {{
                    const el = document.evaluate('{selector.replace("xpath=", "")}', 
                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    return el ? Array.from(el.options).map(o => o.value) : [];
                }}"""
            )
            return options
        except Exception as e:
            print(f"⚠️ Failed to get options from {selector}: {e}")
            return []

    def count_elements(self, selector: str, timeout: Optional[int] = None) -> int:
        """
        Count matching elements.
        
        Args:
            selector: CSS/XPath selector
            timeout: Custom timeout in ms
            
        Returns:
            Number of matching elements
        """
        try:
            timeout = timeout or self.base_timeout
            locator = self.page.locator(selector)
            # Wait a moment for DOM to stabilize
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            return locator.count()
        except Exception as e:
            print(f"⚠️ Failed to count elements {selector}: {e}")
            return 0

    def is_visible(self, selector: str, timeout: int = 1000) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: CSS/XPath selector
            timeout: Check timeout in ms
            
        Returns:
            True if visible, False otherwise
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def extract_text(self, selector: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Extract text content from an element.
        
        Args:
            selector: CSS/XPath selector
            timeout: Custom timeout in ms
            
        Returns:
            Text content or None if extraction fails
        """
        try:
            timeout = timeout or self.base_timeout
            locator = self.wait_for_element(selector, "visible", timeout)
            return locator.text_content()
        except Exception as e:
            print(f"⚠️ Failed to extract text from {selector}: {e}")
            return None

    def wait_for_navigation(self, action: Callable, timeout: int = 30000) -> bool:
        """
        Execute an action and wait for page navigation.
        
        Args:
            action: Callable that triggers navigation
            timeout: Navigation timeout in ms
            
        Returns:
            True if navigation succeeded, False otherwise
        """
        try:
            with self.page.expect_navigation(timeout=timeout):
                action()
            return True
        except PlaywrightTimeoutError:
            print(f"⚠️ Navigation timeout ({timeout}ms)")
            return False
        except Exception as e:
            print(f"⚠️ Navigation error: {e}")
            return False

    def take_screenshot(self, path: str) -> bool:
        """
        Take a screenshot for debugging.
        
        Args:
            path: File path to save screenshot
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.page.screenshot(path=path)
            print(f"📸 Screenshot saved: {path}")
            return True
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return False
