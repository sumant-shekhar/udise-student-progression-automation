import time
import random
from playwright.sync_api import sync_playwright
import helper # our helper functions

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
    
    print("please solve the captcha and click login!")
    input("press enter AFTER you have logged in and see the dashboard...")
    
    # check if we are on dashboard
    if "dashboard" in page.url:
        print("login success!")
        return True
    else:
        print("login failed! page url is:", page.url)
        return False

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
        context = browser.new_context()
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
