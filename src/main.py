"""
Main Orchestrator for UDISE+ Student Progression Automation
Manages authentication, dashboard navigation, and automation loop coordination.
"""

import time
from typing import Optional, Tuple
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from config.settings import USERNAME, PASSWORD, LOGIN_URL, HEADLESS, BROWSER_TYPE, VIEWPORT
from config.settings import WAIT_TIMEOUT, NAVIGATION_TIMEOUT, LOOP_CHECK_INTERVAL
from src.playwright_utils import PlaywrightUtils
from src.progression import ProgressionHandler


class AutomationOrchestrator:
    """Main orchestration class for UDISE+ automation workflows"""

    def __init__(self):
        """Initialize orchestrator with Playwright context"""
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.utils: Optional[PlaywrightUtils] = None
        self.playwright = None

    def setup_browser(self) -> bool:
        """
        Initialize Playwright browser and page.
        
        Returns:
            True if setup successful, False otherwise
        """
        try:
            self.playwright = sync_playwright().start()
            
            # Select browser
            if BROWSER_TYPE == "firefox":
                browser_launcher = self.playwright.firefox
            elif BROWSER_TYPE == "webkit":
                browser_launcher = self.playwright.webkit
            else:
                browser_launcher = self.playwright.chromium
            
            # Launch browser
            self.browser = browser_launcher.launch(headless=HEADLESS)
            self.context = self.browser.new_context(viewport=VIEWPORT)
            self.page = self.context.new_page()
            self.utils = PlaywrightUtils(self.page, base_timeout=WAIT_TIMEOUT)
            
            print(f"🌐 Browser launched ({BROWSER_TYPE})")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False

    def cleanup(self) -> None:
        """Close browser and cleanup resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("✅ Cleanup completed")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

    def login(self) -> bool:
        """
        Perform login to UDISE+ platform.
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            print("\n🔐 Initiating login...")
            
            # Navigate to login page
            self.page.goto(LOGIN_URL, wait_until="domcontentloaded")
            print(f"📄 Navigated to login page")
            
            # Enter credentials
            username_sel = "id=username-field"
            password_sel = "id=password-field"
            submit_sel = "id=submit-btn"
            
            # Fill username
            if not self.utils.safe_input(username_sel, USERNAME):
                print("❌ Failed to enter username")
                return False
            
            # Fill password
            if not self.utils.safe_input(password_sel, PASSWORD):
                print("❌ Failed to enter password")
                return False
            
            print("✅ Credentials entered")
            
            # Allow time for any additional authentication (MFA, etc.)
            print("⏳ Waiting 15 seconds for additional authentication (if any)...")
            time.sleep(15)
            
            # Click submit
            if not self.utils.safe_click(submit_sel, timeout=WAIT_TIMEOUT):
                print("❌ Failed to click login button")
                return False
            
            print("✅ Login button clicked")
            
            # Wait for dashboard load
            print("⏳ Waiting for dashboard to load...")
            self.page.wait_for_load_state("networkidle", timeout=NAVIGATION_TIMEOUT)
            time.sleep(10)  # Additional buffer for dashboard initialization
            
            print("✅ Dashboard loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            self.utils.take_screenshot("/tmp/login_failure.png")
            return False

    def get_student_count(self) -> int:
        """
        Get count of students in current class table.
        
        Returns:
            Number of students (table rows)
        """
        try:
            rows_xpath = "/html/body/app-root/app-admin-dashboard/div[2]/div[2]/main/div/div/div/app-promotion/div[3]/div/table/tbody/tr"
            rows_sel = self.utils.xpath(rows_xpath)
            count = self.utils.count_elements(rows_sel)
            return count
        except Exception as e:
            print(f"⚠️ Failed to get student count: {e}")
            return 0

    def process_class_batch(self) -> Tuple[int, int]:
        """
        Process all students in the currently selected class.
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        try:
            total_students = self.get_student_count()
            
            if total_students == 0:
                print("👀 No students found in current selection")
                return 0, 0
            
            print(f"\n📊 Processing {total_students} students...")
            failed_rows = []
            
            handler = ProgressionHandler(self.page, self.utils)
            
            for row_idx in range(1, total_students + 1):
                try:
                    handler.process_student_row(row_idx, failed_rows)
                except Exception as row_err:
                    print(f"  ❌ Row {row_idx} error: {row_err}")
                    failed_rows.append(row_idx)
                    time.sleep(0.5)
            
            successful = total_students - len(failed_rows)
            print(f"\n🎉 Batch completed: {successful}/{total_students} successful")
            if failed_rows:
                print(f"  ⚠️ Failed rows: {failed_rows}")
            
            return successful, len(failed_rows)
            
        except Exception as e:
            print(f"❌ Batch processing error: {e}")
            return 0, 0

    def run_automation_loop(self) -> None:
        """
        Main automation loop that continuously monitors for new classes and processes them.
        Waits for user to select a class, processes all students, then waits for next class.
        """
        print("\n🚀 Automation loop started")
        print("   Instructions:")
        print("   1. Select a class from the dashboard")
        print("   2. Script will automatically process all students")
        print("   3. After completion, select the next class or press Ctrl+C to exit\n")
        
        total_batches = 0
        total_successful = 0
        total_failed = 0
        
        try:
            while True:
                initial_count = self.get_student_count()
                
                if initial_count == 0:
                    print(f"⏳ Waiting {LOOP_CHECK_INTERVAL}s for class selection...")
                    time.sleep(LOOP_CHECK_INTERVAL)
                    continue
                
                # Process the batch
                successful, failed = self.process_class_batch()
                total_batches += 1
                total_successful += successful
                total_failed += failed
                
                # Wait for next class selection
                print(f"\n⏳ Waiting {LOOP_CHECK_INTERVAL}s for next class selection...")
                time.sleep(LOOP_CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Automation stopped by user")
        except Exception as e:
            print(f"\n❌ Automation error: {e}")
        finally:
            # Print summary
            print(f"\n{'='*50}")
            print(f"📈 AUTOMATION SUMMARY")
            print(f"{'='*50}")
            print(f"  Batches processed: {total_batches}")
            print(f"  Total successful: {total_successful}")
            print(f"  Total failed: {total_failed}")
            print(f"  Success rate: {(total_successful/(total_successful + total_failed)*100):.1f}%" if (total_successful + total_failed) > 0 else "  No students processed")
            print(f"{'='*50}\n")

    def run(self) -> None:
        """Execute the complete automation workflow"""
        try:
            # Setup
            if not self.setup_browser():
                return
            
            # Login
            if not self.login():
                return
            
            # Main loop
            self.run_automation_loop()
            
        except Exception as e:
            print(f"❌ Fatal error: {e}")
        finally:
            self.cleanup()


def main():
    """Entry point for the automation script"""
    print("\n" + "="*60)
    print(" UDISE+ STUDENT PROGRESSION AUTOMATION")
    print(" Playwright-based Enterprise Automation Framework")
    print("="*60 + "\n")
    
    orchestrator = AutomationOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()
