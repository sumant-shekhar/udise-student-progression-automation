"""
Progression Profile Handler
Manages student progression workflows including promotion status, marks, attendance, and section assignment.
"""

import time
import random
from typing import List, Tuple, Optional
from playwright.sync_api import Page

from src.playwright_utils import PlaywrightUtils


class ProgressionHandler:
    """Handles student progression updates through the promotion workflow"""

    def __init__(self, page: Page, utils: PlaywrightUtils):
        """
        Initialize Progression Handler.
        
        Args:
            page: Playwright Page instance
            utils: PlaywrightUtils instance
        """
        self.page = page
        self.utils = utils

    def _get_student_row_base_paths(self, row_index: int) -> Tuple[str, str]:
        """
        Get XPath base paths for a student row.
        
        Args:
            row_index: 1-indexed row number in the table
            
        Returns:
            Tuple of (base_path_td2, base_path_td3)
        """
        base = f"/html/body/app-root/app-admin-dashboard/div[2]/div[2]/main/div/div/div/app-promotion/div[3]/div/table/tbody/tr[{row_index}]/td[2]/ul"
        base_td3 = f"/html/body/app-root/app-admin-dashboard/div[2]/div[2]/main/div/div/div/app-promotion/div[3]/div/table/tbody/tr[{row_index}]/td[3]/ul[2]"
        return base, base_td3

    def set_promotion_status(self, row_index: int) -> bool:
        """
        Set promotion status to "Promoted by Examination".
        
        Args:
            row_index: 1-indexed row number
            
        Returns:
            True if successful, False otherwise
        """
        try:
            base, _ = self._get_student_row_base_paths(row_index)
            selector = self.utils.xpath(f"{base}/li[1]/select")
            
            if self.utils.safe_select(selector, "1"):
                print(f"  ✅ Promotion Status: Promoted (by Examination)")
                return True
            else:
                print(f"  ⚠️ Failed to set promotion status")
                return False
        except Exception as e:
            print(f"  ❌ Promotion status error: {e}")
            return False

    def set_marks(self, row_index: int, marks: Optional[int] = None) -> bool:
        """
        Set student marks (percentage).
        
        Args:
            row_index: 1-indexed row number
            marks: Marks value (60-100), randomized if None
            
        Returns:
            True if successful, False otherwise
        """
        try:
            base, _ = self._get_student_row_base_paths(row_index)
            marks = marks or random.randint(60, 80)
            selector = self.utils.xpath(f"{base}/li[2]/input")
            
            if self.utils.safe_input(selector, str(marks)):
                time.sleep(0.15)
                print(f"  ✅ Marks: {marks}%")
                return True
            else:
                print(f"  ⚠️ Failed to set marks")
                return False
        except Exception as e:
            print(f"  ❌ Marks error: {e}")
            return False

    def set_attendance_days(self, row_index: int, days: Optional[int] = None) -> bool:
        """
        Set attendance days.
        
        Args:
            row_index: 1-indexed row number
            days: Number of days (200-220), randomized if None
            
        Returns:
            True if successful, False otherwise
        """
        try:
            base, _ = self._get_student_row_base_paths(row_index)
            days = days or random.randint(200, 220)
            selector = self.utils.xpath(f"{base}/li[3]/input")
            
            if self.utils.safe_input(selector, str(days)):
                time.sleep(0.15)
                print(f"  ✅ Attendance Days: {days}")
                return True
            else:
                print(f"  ⚠️ Failed to set attendance days")
                return False
        except Exception as e:
            print(f"  ❌ Attendance days error: {e}")
            return False

    def set_schooling_status(self, row_index: int) -> bool:
        """
        Set schooling status (school continuation or transfer status).
        
        Args:
            row_index: 1-indexed row number
            
        Returns:
            True if successful, False otherwise
        """
        try:
            base, _ = self._get_student_row_base_paths(row_index)
            selector = self.utils.xpath(f"{base}/li[4]/select")
            
            # Get available options
            options = self.utils.get_select_options(selector)
            
            if not options:
                print(f"  ⚠️ No schooling status options available, skipping")
                return False
            
            # Prefer "Same School" (value 1), fallback to first available
            target_value = "1" if "1" in options else options[0]
            label = "Same School" if target_value == "1" else "Other Status"
            
            if self.utils.safe_select(selector, target_value):
                print(f"  ✅ Schooling Status: {label}")
                return True
            else:
                print(f"  ⚠️ Failed to set schooling status")
                return False
        except Exception as e:
            print(f"  ⚠️ Schooling status error (non-critical): {e}")
            return False  # Non-critical field

    def set_section(self, row_index: int, section: str = "1") -> bool:
        """
        Set student section.
        
        Args:
            row_index: 1-indexed row number
            section: Section code (default: "1" for Section A)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            _, base_td3 = self._get_student_row_base_paths(row_index)
            selector = self.utils.xpath(f"{base_td3}/li[2]/select")
            
            if self.utils.safe_select(selector, section):
                print(f"  ✅ Section: A")
                return True
            else:
                print(f"  ⚠️ Failed to set section")
                return False
        except Exception as e:
            print(f"  ⚠️ Section error (non-critical): {e}")
            return False  # Non-critical field

    def click_update_button(self, row_index: int, max_retries: int = 3) -> bool:
        """
        Click the update button for a student row.
        
        Args:
            row_index: 1-indexed row number
            max_retries: Number of retry attempts
            
        Returns:
            True if successful, False otherwise
        """
        update_selector = self.utils.xpath(
            f"/html/body/app-root/app-admin-dashboard/div[2]/div[2]/main/div/div/div/app-promotion/div[3]/div/table/tbody/tr[{row_index}]/td[6]/button[1]"
        )
        
        if self.utils.safe_click(update_selector, max_retries=max_retries):
            print(f"  ✅ Update button clicked")
            return True
        else:
            print(f"  ❌ Update button click failed after {max_retries} retries")
            return False

    def confirm_dialog(self, timeout: int = 5000) -> bool:
        """
        Confirm the SweetAlert2 confirmation dialog.
        
        Args:
            timeout: Dialog wait timeout in ms
            
        Returns:
            True if dialog confirmed, False otherwise
        """
        try:
            # Wait for dialog and click confirm button
            if self.utils.safe_click(".swal2-confirm", timeout=timeout):
                print(f"  ✅ Confirmation dialog accepted")
                time.sleep(0.5)  # Wait for response processing
                return True
            else:
                print(f"  ⚠️ Confirmation dialog not found or click failed")
                return False
        except Exception as e:
            print(f"  ⚠️ Dialog confirmation error: {e}")
            return False

    def process_student_row(self, row_index: int, failed_rows: List[int]) -> bool:
        """
        Process a complete student row through all progression steps.
        
        Args:
            row_index: 1-indexed row number
            failed_rows: List to append failed row indices to
            
        Returns:
            True if all steps completed successfully, False otherwise
        """
        print(f"\n── Row {row_index} ──")
        
        try:
            # Step 1: Promotion Status
            if not self.set_promotion_status(row_index):
                failed_rows.append(row_index)
                return False
            
            # Step 2: Marks
            if not self.set_marks(row_index):
                failed_rows.append(row_index)
                return False
            
            # Step 3: Attendance Days
            if not self.set_attendance_days(row_index):
                failed_rows.append(row_index)
                return False
            
            # Step 4: Schooling Status (non-critical)
            self.set_schooling_status(row_index)
            
            # Step 5: Section (non-critical)
            self.set_section(row_index)
            
            # Step 6: Update Button
            if not self.click_update_button(row_index):
                failed_rows.append(row_index)
                return False
            
            # Step 7: Confirm Dialog
            if not self.confirm_dialog():
                failed_rows.append(row_index)
                return False
            
            print(f"  🎉 Row {row_index} completed successfully")
            return True
            
        except Exception as e:
            print(f"  ❌ Row {row_index} processing failed: {e}")
            failed_rows.append(row_index)
            return False
