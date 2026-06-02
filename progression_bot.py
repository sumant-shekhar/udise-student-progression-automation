import time
from playwright.sync_api import sync_playwright
import helper

# user details
USER = "10140806703"
PASS = "Pankaj@123.123"

def login(page):
    print("logging in to progression site...")
    page.goto("https://sdms.udiseplus.gov.in/p0/v1/login?state-id=110")
    
    helper.wait_and_type(page, "//input[@id='username-field']", USER)
    helper.wait_and_type(page, "//input[@id='password-field']", PASS)
    
    print("waiting 15 seconds for captcha...")
    time.sleep(15)
    
    # try to click login
    try:
        if page.locator("xpath=//button[@id='submit-btn']").is_visible():
            page.click("xpath=//button[@id='submit-btn']")
    except:
        pass

    input("press enter AFTER you see the dashboard...")
    
    print("login worked!")
    return True

def process_student_row(page, row_num):
    print(f"processing student row {row_num}")
    try:
        # this is hardcoded xpath for the table rows
        base_xpath = f"/html/body/app-root/app-admin-dashboard/div[2]/div[2]/main/div/div/div/app-promotion/div[3]/div/table/tbody/tr[{row_num}]"
        
        # select progression status (Promoted)
        status_xpath = f"{base_xpath}/td[3]/select"
        helper.select_option(page, f"xpath={status_xpath}", "1") # 1 = Promoted
        
        # enter marks
        marks = helper.get_random_val(60, 95) # random marks between 60-95
        marks_xpath = f"{base_xpath}/td[4]/input"
        helper.wait_and_type(page, marks_xpath, marks)
        
        # enter days
        days = helper.get_random_val(200, 220) # random days between 200-220
        days_xpath = f"{base_xpath}/td[5]/input"
        helper.wait_and_type(page, days_xpath, days)
        
        # select schooling status
        schooling_xpath = f"{base_xpath}/td[6]/select"
        helper.select_option(page, f"xpath={schooling_xpath}", "1") # 1 = Studying in same school
        
        # click update
        update_btn_xpath = f"{base_xpath}/td[8]/button"
        helper.wait_and_click(page, update_btn_xpath)
        
        print(f"row {row_num} updated!")
        return True
    except Exception as e:
        print(f"error on row {row_num}: {e}")
        return False

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        if login(page):
            print("please select the class and section now.")
            input("press enter when students are visible...")
            
            # loop through students
            for i in range(1, 100): # try up to 100 students
                success = process_student_row(page, i)
                if not success:
                    print("stopped or finished the list.")
                    break
                time.sleep(1)
            
            input("finished! press enter to close browser...")
                
        browser.close()

if __name__ == "__main__":
    main()
