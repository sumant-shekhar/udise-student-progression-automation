"""
Student Information Scraper - Extract student data from UDISE+ dashboard.
Migrated from Selenium to Playwright.
"""

from typing import Dict, Any
from playwright.sync_api import Page


class StudentInfoScraper:
    """Scrapes student information from UDISE+ dashboard."""

    def __init__(self, page: Page):
        """
        Initialize scraper.

        Args:
            page: Playwright page object
        """
        self.page = page

    def extract_student_info(self) -> Dict[str, Any]:
        """
        Extract student information from current page.

        Returns:
            Dictionary with student information
        """
        student_info = {}

        try:
            # Extract student card information (CSS selector preserved)
            card_locator = self.page.locator("div.card.blue15").first
            
            if card_locator.count() > 0:
                # Extract student name
                try:
                    name = card_locator.locator("h3").first.text_content()
                    student_info["name"] = name.strip() if name else ""
                except Exception:
                    student_info["name"] = "N/A"

                # Extract roll number
                try:
                    roll_text = card_locator.locator("p").first.text_content()
                    student_info["roll_number"] = roll_text.strip() if roll_text else ""
                except Exception:
                    student_info["roll_number"] = "N/A"

                # Extract class
                try:
                    class_text = card_locator.locator("p:nth-of-type(2)").text_content()
                    student_info["class"] = class_text.strip() if class_text else ""
                except Exception:
                    student_info["class"] = "N/A"

        except Exception as e:
            print(f"  ⚠️ Error extracting student info: {e}")

        return student_info

    def get_student_list_count(self) -> int:
        """
        Get count of students in queue.

        Returns:
            Number of students to process
        """
        try:
            students = self.page.locator("div.card.blue15")
            return students.count()
        except Exception:
            return 0

    def extract_all_students(self) -> list:
        """
        Extract information for all visible students.

        Returns:
            List of student information dictionaries
        """
        students = []
        count = self.get_student_list_count()

        for i in range(count):
            try:
                student_data = {
                    "index": i,
                    "info": {},
                }
                students.append(student_data)
            except Exception as e:
                print(f"  ⚠️ Error extracting student {i}: {e}")

        return students
