from playwright.sync_api import sync_playwright
import time
import random

# basic helpers for the bot
def wait_and_click(page, xpath):
    # wait for element and click it
    page.wait_for_selector(f"xpath={xpath}")
    page.click(f"xpath={xpath}")
    time.sleep(0.5)

def wait_and_type(page, xpath, text):
    # wait and type text
    page.wait_for_selector(f"xpath={xpath}")
    page.fill(f"xpath={xpath}", "")
    page.type(f"xpath={xpath}", text)
    time.sleep(0.3)

def select_option(page, selector, value):
    # select from dropdown
    page.wait_for_selector(selector)
    page.select_option(selector, value)
    time.sleep(0.2)

def scroll_down(page):
    # scroll to bottom of page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(0.5)
