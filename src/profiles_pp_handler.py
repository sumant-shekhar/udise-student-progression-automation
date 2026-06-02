"""
Profile Preview Complete - Final preview and submission of student profile.
Migrated from Selenium to Playwright with XPath selectors preserved.
"""

import time
from typing import Dict, Any
from playwright.sync_api import Page
from profiles_playwright_utils import ProfilePlaywrightUtils


class ProfilePreviewComplete:
    """Handles final profile preview and submission."""

    def __init__(self, page: Page, utils: ProfilePlaywrightUtils):
        """
        Initialize Profile Preview Complete.

        Args:
            page: Playwright page object
            utils: ProfilePlaywrightUtils instance
        """
        self.page = page
        self.utils = utils

    def update(self, student_log: Dict[str, Any]) -> None:
        """
        Review and confirm final profile submission.

        Args:
            student_log: Dictionary to log student data
        """
        try:
            # Scroll to view all profile data
            self.utils.scroll_to_bottom()
            time.sleep(0.5)

            # Extract profile summary (if needed)
            print("  📋 Reviewing profile summary...")
            time.sleep(0.3)

            # Click submit/confirm button (XPath preserved)
            submit_button_xpath = "//button[normalize-space(span/text())='Submit']"
            if self.utils.element_exists(submit_button_xpath):
                self.utils.js_click(submit_button_xpath)
                time.sleep(0.2)
                print("  ✅ Profile submitted")
            else:
                # Try alternative button names
                for button_text in ["Complete", "Finish", "Done"]:
                    alt_xpath = f"//button[normalize-space(span/text())='{button_text}']"
                    if self.utils.element_exists(alt_xpath):
                        self.utils.js_click(alt_xpath)
                        time.sleep(0.2)
                        print(f"  ✅ Profile completed via '{button_text}' button")
                        break

        except Exception as e:
            print(f"  ❌ Profile submission error: {e}")

        # Confirm SweetAlert2 confirmation dialog
        try:
            time.sleep(0.5)
            confirm_css = "div.swal2-actions > button.swal2-confirm"
            if self.utils.page.locator(confirm_css).count() > 0:
                self.utils.js_click_css(confirm_css)
                time.sleep(0.3)
                print("  ✅ Confirmation dialog accepted")
        except Exception as e:
            print(f"  ⚠️ Confirmation dialog not found: {e}")

        # Navigate to next student or exit
        try:
            next_button_xpath = "//button[normalize-space(text())='Next Student']"
            if self.utils.element_exists(next_button_xpath):
                self.utils.js_click(next_button_xpath)
                time.sleep(0.5)
                print("  ✅ Moving to next student...")
                return True
            else:
                print("  ℹ️ No more students or end of batch reached")
                return False
        except Exception as e:
            print(f"  ⚠️ Navigation error: {e}")
            return False

    def get_profile_data(self) -> Dict[str, Any]:
        """
        Extract visible profile data from preview screen.

        Returns:
            Dictionary of profile data
        """
        profile_data = {}
        try:
            # Extract visible profile fields (adjust XPaths as needed for your form)
            sections = [
                "General Profile",
                "Enrolment Profile",
                "Facility Profile",
            ]

            for section in sections:
                section_xpath = f"//h3[contains(text(), '{section}')]"
                if self.utils.element_exists(section_xpath):
                    profile_data[section] = "Present"

        except Exception as e:
            print(f"  ⚠️ Error extracting profile data: {e}")

        return profile_data
