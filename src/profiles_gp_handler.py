"""
General Profile Updater - Updates phone number and blood group.
Migrated from Selenium to Playwright with XPath selectors preserved.
"""

import time
import random
from typing import Dict, Any
from playwright.sync_api import Page
from profiles_playwright_utils import ProfilePlaywrightUtils


class GeneralProfileUpdater:
    """Updates general student profile information (phone number, blood group)."""

    def __init__(self, page: Page, utils: ProfilePlaywrightUtils):
        """
        Initialize General Profile Updater.

        Args:
            page: Playwright page object
            utils: ProfilePlaywrightUtils instance
        """
        self.page = page
        self.utils = utils

    def update(self, student_log: Dict[str, Any]) -> None:
        """
        Update general profile for student.

        Args:
            student_log: Dictionary to log student data
        """
        try:
            phone_input = self.utils.wait_for_element("//input[@id='phoneNo']")
            current_value = self.utils.get_input_value("//input[@id='phoneNo']")

            if current_value in ("9999999991", "9999999999") or not current_value:
                self.utils.safe_input("//input[@id='phoneNo']", "")
                full_number = "97855" + str(random.randint(10000, 99999))
                self.utils.safe_input("//input[@id='phoneNo']", full_number)
                student_log["phone"] = full_number
            else:
                student_log["phone"] = current_value
        except Exception as e:
            print(f"  ❌ Phone number error: {e}")

        time.sleep(0.2)
        self.utils.scroll_to_bottom()
        time.sleep(0.3)

        try:
            blood_group_value = self.utils.get_selected_option_value("select[formcontrolname='bloodGroup']")
            if blood_group_value == "":
                self.utils.select_by_value("select[formcontrolname='bloodGroup']", "9")
        except Exception as e:
            print(f"  ❌ Blood group error: {e}")

        # Save button: //button[normalize-space(span/text())='Save']
        self.utils.js_click("//button[normalize-space(span/text())='Save']")
        time.sleep(0.2)
        print("  ✅ General Profile saved")

        # SweetAlert2 confirm button
        self.utils.js_click_css("div.swal2-actions > button.swal2-confirm")
        time.sleep(0.2)

        # Next step button
        self.utils.js_click("//button[@type='button' and @matsteppernext]")
        time.sleep(0.2)
        print("  ✅ Moved to Enrolment Profile tab")
