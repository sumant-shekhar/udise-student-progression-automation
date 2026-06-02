"""
Profile Automation Orchestrator - Main entry point for student profile automation.
Migrated from Selenium to Playwright, all XPath/CSS selectors preserved.
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page
from profiles_playwright_utils import ProfilePlaywrightUtils
from profiles_gp_handler import GeneralProfileUpdater
from profiles_ep_handler import EnrolmentProfileUpdater
from profiles_fp_handler import FacilityProfileUpdater
from profiles_pp_handler import ProfilePreviewComplete


class ProfileAutomationOrchestrator:
    """Main orchestrator for student profile automation workflow."""

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        browser_type: str = "chromium",
    ):
        """
        Initialize orchestrator.

        Args:
            username: UDISE+ username
            password: UDISE+ password
            headless: Run in headless mode
            browser_type: Browser type (chromium, firefox, webkit)
        """
        self.username = username
        self.password = password
        self.headless = headless
        self.browser_type = browser_type
        self.page: Page = None
        self.browser = None
        self.context = None
        self.utils: ProfilePlaywrightUtils = None

        # Initialize handlers
        self.gp_updater: GeneralProfileUpdater = None
        self.ep_updater: EnrolmentProfileUpdater = None
        self.fp_updater: FacilityProfileUpdater = None
        self.pp_updater: ProfilePreviewComplete = None

        # Statistics
        self.stats = {
            "students_processed": 0,
            "successful": 0,
            "failed": 0,
            "start_time": None,
            "end_time": None,
        }

    def setup_browser(self) -> None:
        """Initialize Playwright browser and page."""
        playwright = sync_playwright().start()

        if self.browser_type == "chromium":
            self.browser = playwright.chromium.launch(headless=self.headless)
        elif self.browser_type == "firefox":
            self.browser = playwright.firefox.launch(headless=self.headless)
        elif self.browser_type == "webkit":
            self.browser = playwright.webkit.launch(headless=self.headless)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        self.page = self.context.new_page()
        self.utils = ProfilePlaywrightUtils(self.page, wait_timeout=20000)

        # Initialize handlers
        self.gp_updater = GeneralProfileUpdater(self.page, self.utils)
        self.ep_updater = EnrolmentProfileUpdater(self.page, self.utils)
        self.fp_updater = FacilityProfileUpdater(self.page, self.utils)
        self.pp_updater = ProfilePreviewComplete(self.page, self.utils)

        print("✅ Browser initialized")

    def close_browser(self) -> None:
        """Close browser and cleanup."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        print("✅ Browser closed")

    def login(self) -> bool:
        """
        Perform UDISE+ login with CAPTCHA wait.

        Returns:
            True if login successful, False otherwise
        """
        try:
            login_url = "https://sdms.udiseplus.gov.in/p0/v1/login?state-id=110"
            print(f"🔗 Navigating to {login_url}")
            self.page.goto(login_url, wait_until="networkidle")
            self.page.set_viewport_size(width=1920, height=1080)

            # Fill username
            username_field_xpath = "//input[@id='username-field']"
            self.utils.safe_input(username_field_xpath, self.username)
            time.sleep(0.3)

            # Fill password
            password_field_xpath = "//input[@id='password-field']"
            self.utils.safe_input(password_field_xpath, self.password)
            time.sleep(0.3)

            print("⏳ Please solve CAPTCHA in browser (waiting 20 seconds)...")
            time.sleep(20)

            # Check if logged in
            try:
                self.page.wait_for_url("**/dashboard**", timeout=30000)
                print("✅ Login successful")
                return True
            except Exception:
                print("❌ Login failed or CAPTCHA not solved")
                return False

        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def process_student(self, student_index: int) -> bool:
        """
        Process single student profile through all steps.

        Args:
            student_index: Student index in batch

        Returns:
            True if successful, False otherwise
        """
        student_log = {
            "index": student_index,
            "timestamp": datetime.now().isoformat(),
        }

        try:
            print(f"\n📚 Processing Student #{student_index + 1}...")

            # Step 1: General Profile
            print("  Step 1: General Profile (GP)")
            self.gp_updater.update(student_log)
            time.sleep(0.5)

            # Step 2: Enrolment Profile
            print("  Step 2: Enrolment Profile (EP)")
            self.ep_updater.update(student_log)
            time.sleep(0.5)

            # Step 3: Facility Profile
            print("  Step 3: Facility Profile (FP)")
            self.fp_updater.update(student_log)
            time.sleep(0.5)

            # Step 4: Profile Preview
            print("  Step 4: Profile Preview (PP)")
            self.pp_updater.update(student_log)
            time.sleep(0.5)

            student_log["status"] = "completed"
            self.stats["successful"] += 1
            print(f"  ✅ Student #{student_index + 1} completed successfully")
            return True

        except Exception as e:
            student_log["status"] = "failed"
            student_log["error"] = str(e)
            self.stats["failed"] += 1
            print(f"  ❌ Student #{student_index + 1} processing failed: {e}")
            return False

    def run_automation_loop(self, max_students: int = None) -> None:
        """
        Run continuous automation loop.

        Args:
            max_students: Maximum students to process (None for unlimited)
        """
        self.stats["start_time"] = datetime.now()

        try:
            student_count = 0
            while True:
                if max_students and student_count >= max_students:
                    print(f"\n📊 Reached maximum students limit ({max_students})")
                    break

                try:
                    # Check if next student is available
                    next_btn = self.page.locator("//button[normalize-space(text())='Next Student']")
                    if next_btn.count() == 0:
                        print("\n✅ No more students in queue")
                        break

                    # Process student
                    success = self.process_student(student_count)
                    self.stats["students_processed"] += 1

                    if not success:
                        print("  ⚠️ Continuing to next student despite error...")

                    student_count += 1
                    time.sleep(1)

                except KeyboardInterrupt:
                    print("\n\n⏹️ Automation stopped by user")
                    break
                except Exception as e:
                    print(f"  ❌ Unexpected error in loop: {e}")
                    time.sleep(2)
                    continue

        finally:
            self.stats["end_time"] = datetime.now()
            self.print_statistics()

    def print_statistics(self) -> None:
        """Print session statistics."""
        print("\n" + "=" * 60)
        print("📊 AUTOMATION SESSION STATISTICS")
        print("=" * 60)
        print(f"Students Processed: {self.stats['students_processed']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")

        if self.stats["start_time"] and self.stats["end_time"]:
            duration = self.stats["end_time"] - self.stats["start_time"]
            print(f"Duration: {duration}")

        if self.stats["students_processed"] > 0:
            success_rate = (
                self.stats["successful"] / self.stats["students_processed"] * 100
            )
            print(f"Success Rate: {success_rate:.1f}%")

        print("=" * 60 + "\n")


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    username = os.getenv("UDISE_USERNAME", "10140615303")
    password = os.getenv("UDISE_PASSWORD", "58#wwhLG")

    print("🚀 UDISE+ Student Profile Automation")
    print("=" * 60)
    print(f"Browser: Chromium")
    print(f"Headless: False")
    print("=" * 60 + "\n")

    orchestrator = ProfileAutomationOrchestrator(
        username=username,
        password=password,
        headless=False,
        browser_type="chromium",
    )

    try:
        # Setup
        orchestrator.setup_browser()

        # Login
        if not orchestrator.login():
            print("❌ Failed to login. Exiting.")
            return

        # Run automation
        orchestrator.run_automation_loop(max_students=None)

    except KeyboardInterrupt:
        print("\n\n⏹️ Automation interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        orchestrator.close_browser()


if __name__ == "__main__":
    main()
