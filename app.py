import time
import random
from playwright.sync_api import sync_playwright
import helper # our helper functions
import captcha_sol

# settings
USERNAME = "10140615303"
PASSWORD = "58#wwhLG"

def login(page):
    print("logging in...")
    page.goto("https://sdms.udiseplus.gov.in/p0/v1/login?state-id=110")
    
    # enter username
    helper.wait_and_type(page, "//input[@id='username-field']", USERNAME)
    # enter password
    helper.wait_and_type(page, "//input[@id='password-field']", PASSWORD)
    
    # try automatic captcha solve
    # real IDs: image=captchaImage, input=captcha
    captcha_sol.solve_captcha(page, "//img[@id='captchaImage']", "//input[@id='captcha']")
    
    print("waiting 15 seconds for you to solve captcha (or script will try)...")
    time.sleep(15)
    
    # try to click login button automatically
    try:
        # try common selectors for the login button
        login_selectors = [
            "//button[@id='submit-btn']",
            "//input[@id='submit-btn']",
            "//button[contains(text(), 'Login')]",
            "//button[normalize-space()='Login']"
        ]
        for sel in login_selectors:
            if page.locator(f"xpath={sel}").is_visible():
                page.click(f"xpath={sel}")
                print(f"clicked login button using {sel}")
                break
    except:
        print("couldnt click login button automatically, please click it yourself if needed")

    input("press enter AFTER you are on the student list page...")
    
    print("ok, starting the process!")
    return True

def update_general_profile(page):
    print("doing step 1: general profile")
    try:
        # check phone number
        phone = page.locator("xpath=//input[@id='phoneNo']").input_value()
        if phone == "9999999991" or phone == "9999999999" or phone == "":
            new_phone = "97855" + str(random.randint(10000, 99999))
            helper.wait_and_type(page, "//input[@id='phoneNo']", new_phone)
        
        helper.scroll_down(page)
        
        # select blood group if empty
        bg = page.locator("select[formcontrolname='bloodGroup']").input_value()
        if bg == "":
            helper.select_option(page, "select[formcontrolname='bloodGroup']", "9") # 9 is for unknown
            
        # click save
        helper.wait_and_click(page, "//button[normalize-space(span/text())='Save']")
        time.sleep(1)
        
        # click ok on alert
        page.click("button.swal2-confirm")
        time.sleep(1)
        
        # click next
        helper.wait_and_click(page, "//button[@type='button' and @matsteppernext]")
        return True
    except Exception as e:
        print("error in step 1:", e)
        return False

def update_enrolment_profile(page):
    print("doing step 2: enrolment profile")
    try:
        helper.scroll_down(page)
        # just click save
        helper.wait_and_click(page, "//button[normalize-space(span/text())='Save']")
        time.sleep(1)
        page.click("button.swal2-confirm")
        time.sleep(1)
        # click next
        helper.wait_and_click(page, "//button[@type='button' and @matsteppernext]")
        return True
    except Exception as e:
        print("error in step 2:", e)
        return False

def update_facility_profile(page):
    print("doing step 3: facility profile")
    try:
        helper.scroll_down(page)
        # click save
        helper.wait_and_click(page, "//button[normalize-space(span/text())='Save']")
        time.sleep(1)
        page.click("button.swal2-confirm")
        time.sleep(1)
        # click next
        helper.wait_and_click(page, "//button[@type='button' and @matsteppernext]")
        return True
    except Exception as e:
        print("error in step 3:", e)
        return False

def complete_preview(page):
    print("doing step 4: preview")
    try:
        helper.scroll_down(page)
        # click complete data
        helper.wait_and_click(page, "//button[normalize-space(text())='Complete Data']")
        time.sleep(1)
        # confirm alert
        page.click("button.swal2-confirm")
        time.sleep(1)
        page.click("button.swal2-confirm") # double confirm
        print("student done!")
        return True
    except Exception as e:
        print("error in step 4:", e)
        return False

def start():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        if not login(page):
            return
            
        print("ready to process students. please go to the student list page.")
        input("press enter once you are on the list page...")
        
        count = 0
        while True:
            print(f"processing student {count+1}")
            
            # click on the student to open profile (assuming we are on the list)
            # here we might need logic to find the first 'Not Started' student
            
            if not update_general_profile(page): break
            if not update_enrolment_profile(page): break
            if not update_facility_profile(page): break
            if not complete_preview(page): break
            
            # click next student
            try:
                helper.wait_and_click(page, "//button[normalize-space(text())='Next Student']")
                count += 1
            except:
                print("no more students or error finding next button")
                break
                
        print(f"done! processed {count} students")
        input("all done! press enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    start()
