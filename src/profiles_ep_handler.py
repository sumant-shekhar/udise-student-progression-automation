"""
Enrolment Profile Updater - Updates admission number, medium, languages, and subjects.
Migrated from Selenium to Playwright with XPath selectors preserved.
"""

import time
import random
from typing import Dict, Any
from playwright.sync_api import Page
from profiles_playwright_utils import ProfilePlaywrightUtils


class EnrolmentProfileUpdater:
    """Updates enrolment profile information (admission, medium, languages, subjects)."""

    def __init__(self, page: Page, utils: ProfilePlaywrightUtils):
        """
        Initialize Enrolment Profile Updater.

        Args:
            page: Playwright page object
            utils: ProfilePlaywrightUtils instance
        """
        self.page = page
        self.utils = utils

    def update(self, student_log: Dict[str, Any]) -> None:
        """
        Update enrolment profile for student.

        Args:
            student_log: Dictionary to log student data
        """
        self.utils.scroll_to_bottom()
        time.sleep(0.2)

        # Update admission number
        try:
            adm_value = self.utils.get_input_value("//input[@id='admNo']")
            if not adm_value.strip():
                adm_no = str(random.randint(10, 99))
                self.utils.safe_input("//input[@id='admNo']", adm_no)
                student_log["admission_no"] = adm_no
        except Exception as e:
            print(f"  ❌ Admission number error: {e}")

        time.sleep(0.2)

        # Update medium of instruction
        try:
            med_value = self.utils.get_selected_option_text("select[id='medium']")
            if med_value.strip().lower() == "select":
                self.utils.select_by_text("select[id='medium']", "4-Hindi")
        except Exception as e:
            print(f"  ❌ Medium of Instruction error: {e}")

        # Update language group
        try:
            lang_select_el = self.page.locator("select[id='languageGroup']").first
            lang_select_el.wait_for(state="attached", timeout=5000)
            try:
                self.utils.select_by_text("select[id='languageGroup']", "English_Hindi_Sanskrit")
            except Exception:
                self.utils.select_by_text("select[id='languageGroup']", "Hindi_English_Sanskrit")
        except Exception as e:
            print(f"  ❌ Language group error: {e}")

        time.sleep(0.2)

        # RTE 12C checkbox (XPath preserved exactly)
        try:
            self.utils.js_click(
                '/html/body/app-root/app-admin-dashboard/div[2]/div[2]/main/div/div/div/app-edit-student-new-ac/div/div/div/div/div[2]/div/mat-stepper/div/div[2]/div[2]/form/div/app-enrolment-edit-new-ac/div/div/div/form/div[1]/div/div/div[10]/div/div[2]/div[2]/input'
            )
        except Exception as e:
            print(f"  ⚠️ RTE 12C not found, skipping: {e}")

        time.sleep(0.2)

        # Handle academic stream and subject selection
        try:
            stream_select_el = self.utils.wait_for_element("//select[@formcontrolname='academicStream']")
            selected_stream = self.utils.get_attribute(
                "//select[@formcontrolname='academicStream']/option[@selected]",
                "value"
            )

            subject_options = {
                "1": ["Geography", "History", "Economics"],
                "2": ["Physics", "Chemistry", "Mathematics"]
            }

            if selected_stream in subject_options:
                # Click dropdown button
                dropdown_btn_xpath = "//ng-multiselect-dropdown[@formcontrolname='subjectGroup']//span[contains(@class,'dropdown-btn')]"
                self.utils.js_click(dropdown_btn_xpath)
                time.sleep(0.3)

                # Select subjects
                for subject in subject_options[selected_stream]:
                    try:
                        option_xpath = f"//div[contains(@class,'dropdown-list')]//div[normalize-space(text())='{subject}']"
                        option_el = self.utils.wait_for_element(option_xpath)
                        self.page.evaluate("(el) => el.click();", option_el)
                        time.sleep(0.2)
                    except Exception as e:
                        print(f"  ⚠️ Subject {subject} not found: {e}")

                # Close dropdown
                self.utils.js_click(dropdown_btn_xpath)
                time.sleep(0.2)

        except Exception as e:
            print(f"  ❌ Subject selection error: {e}")

        time.sleep(0.2)

        # Save button
        self.utils.js_click("//button[normalize-space(span/text())='Save']")
        time.sleep(0.2)
        print("  ✅ Enrolment Profile saved")

        # SweetAlert2 confirm button
        self.utils.js_click_css("div.swal2-actions > button.swal2-confirm")
        time.sleep(0.2)

        # Next step button
        self.utils.js_click("//button[@type='button' and @matsteppernext]")
        time.sleep(0.2)
        print("  ✅ Moved to Facility Profile tab")
