"""
Facility Profile Updater - Updates facility information and health/disability data.
Migrated from Selenium to Playwright with XPath selectors preserved.
"""

import time
from typing import Dict, Any
from playwright.sync_api import Page
from profiles_playwright_utils import ProfilePlaywrightUtils

# Class data for height/weight standards
CLASS_DATA = {
    1: {"height_cm": 115, "weight_kg": 21},
    2: {"height_cm": 122, "weight_kg": 23},
    3: {"height_cm": 128, "weight_kg": 26},
    4: {"height_cm": 133, "weight_kg": 29},
    5: {"height_cm": 138, "weight_kg": 32},
    6: {"height_cm": 144, "weight_kg": 36},
    7: {"height_cm": 149, "weight_kg": 40},
    8: {"height_cm": 156, "weight_kg": 45},
    9: {"height_cm": 164, "weight_kg": 51},
    10: {"height_cm": 170, "weight_kg": 56},
}

CLASS_NAME_MAP = {
    "lkg": 1,
    "ukg": 1,
    "kg1": 1,
    "kg2": 1,
    "pp1": 1,
    "pp2": 1,
    "nursery": 1,
    "pre-primary": 1,
    "preprimary": 1,
    "i": 1,
    "ii": 2,
    "iii": 3,
    "iv": 4,
    "v": 5,
    "vi": 6,
    "vii": 7,
    "viii": 8,
    "ix": 9,
    "x": 10,
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
}


def get_class_number(class_str: str) -> int:
    """
    Convert class string to class number for height/weight mapping.

    Args:
        class_str: Class string (e.g., "VI", "6", "Class VI")

    Returns:
        Class number (1-10) or 5 as default
    """
    if not class_str:
        return 5
    for token in class_str.replace("-", "").split("/"):
        key = token.strip().lower()
        if key in CLASS_NAME_MAP:
            return CLASS_NAME_MAP[key]
    return 5


class FacilityProfileUpdater:
    """Updates facility profile information (health, disabilities, facilities)."""

    def __init__(self, page: Page, utils: ProfilePlaywrightUtils):
        """
        Initialize Facility Profile Updater.

        Args:
            page: Playwright page object
            utils: ProfilePlaywrightUtils instance
        """
        self.page = page
        self.utils = utils

    def update(self, student_log: Dict[str, Any]) -> None:
        """
        Update facility profile for student.

        Args:
            student_log: Dictionary to log student data
        """
        # Select "Yes" for facility provision
        try:
            yes_radio_xpath = "//input[@type='radio' and @formcontrolname='facProvYN' and @value='1']"
            yes_radio = self.utils.wait_for_element(yes_radio_xpath)
            self.page.evaluate("(el) => el.click();", yes_radio)
            time.sleep(0.2)

            # Click textbook checkbox
            textbook_checkbox_xpath = "//input[@type='checkbox' and @id='textbook']"
            textbook_checkbox = self.utils.wait_for_element(textbook_checkbox_xpath)
            textbook_checkbox.click()
            time.sleep(0.2)
        except Exception as e:
            print(f"  ❌ Facility YES/TextBook error: {e}")

        # CWSN selection
        try:
            self.utils.js_click_css("input[formcontrolname='cwsnYN'][value='2']")
        except Exception as e:
            print(f"  ❌ CWSN error: {e}")
        time.sleep(0.2)

        # Set various disability and program fields to "No" (value='2')
        for field_name in [
            "screenedForSld",
            "autismSpectrumDisorder",
            "attentionDeficitHyperactiveDisorder",
            "giftedChildrenYn",
            "olympdsNlc",
            "nccNssYn",
        ]:
            try:
                radio_xpath = f"//input[@type='radio' and @formcontrolname='{field_name}' and @value='2']"
                radio = self.utils.wait_for_element(radio_xpath)
                self.page.evaluate("(el) => el.click();", radio)
                time.sleep(0.15)
            except Exception as e:
                print(f"  ⚠️ {field_name} error: {e}")

        time.sleep(0.2)

        # Height/Weight section (if class number available)
        if "class_number" in student_log:
            class_num = student_log["class_number"]
            if class_num in CLASS_DATA:
                height = CLASS_DATA[class_num]["height_cm"]
                weight = CLASS_DATA[class_num]["weight_kg"]

                try:
                    height_xpath = "//input[@id='height']"
                    self.utils.safe_input(height_xpath, str(height))
                    time.sleep(0.2)

                    weight_xpath = "//input[@id='weight']"
                    self.utils.safe_input(weight_xpath, str(weight))
                    time.sleep(0.2)
                    print(f"  ✅ Height/Weight set to {height}cm/{weight}kg for class {class_num}")
                except Exception as e:
                    print(f"  ⚠️ Height/Weight error: {e}")

        time.sleep(0.2)

        # Save button
        self.utils.js_click("//button[normalize-space(span/text())='Save']")
        time.sleep(0.2)
        print("  ✅ Facility Profile saved")

        # SweetAlert2 confirm button
        self.utils.js_click_css("div.swal2-actions > button.swal2-confirm")
        time.sleep(0.2)

        # Next step button
        self.utils.js_click("//button[@type='button' and @matsteppernext]")
        time.sleep(0.2)
        print("  ✅ Moved to Profile Preview tab")
