# Student Progression Bot

this bot helps to fill student data on udise plus website automatically. i made this because doing it manually takes too much time.

## how to use

1. install python
2. install playwright: `pip install playwright`
3. install browsers: `playwright install chromium`
4. edit the username and password in `app.py` or `progression_bot.py`
5. run it: `python app.py`

## files
- `app.py`: for student profile entry (GP, EP, FP, PP)
- `progression_bot.py`: for student promotion/progression (marks and days)
- `helper.py`: contains common functions like wait_and_click
- `get_xpaths.py`: run this and click buttons to find their xpaths
- `captcha_sol.py`: trying to solve captcha with AI/OCR

## automatic captcha (if you want)
if you want the script to try solving captcha by itself:
1. install tesseract: `sudo apt update && sudo apt install tesseract-ocr`
2. install python tools: `pip install pytesseract pillow`
*if you get permission error run this first:* `sudo chown -R $USER:$USER .venv`

## finding new buttons
if the website changes and buttons stop working:
1. run `python3 get_xpaths.py`
2. click the buttons in the browser that opens
3. look at `found_xpaths.txt` to see the new paths

## note
- the script waits 15 seconds for captcha. you can solve it yourself or wait for the script.
- press ENTER in the terminal only when you are on the correct page!

## app.py logic

This file is used for:
```
1. doing step 1: general profile
   a. check phone number (if 999... then change it)
   b. select blood group if empty
   c. click save
   d. click ok on alert
   e. click next

2. doing step 2: enrolment profile
   a. scroll down to bottom
   b. click save
   c. click ok on alert
   d. click next

3. doing step 3: facility profile
   a. scroll down to bottom
   b. click save
   c. click ok on alert
   d. click next

4. doing step 4: preview
   a. scroll down to bottom
   b. click complete data
   c. confirm alert
   d. double confirm alert
```
and basic browser stuff login and student loop.

## progression_bot.py logic
This file is for the promotion page:
1. select progression status (Promoted)
2. enter marks (65%)
3. enter number of days (210)
4. select schooling status (Same school)
5. click update button
it loops through all rows in the table until it finishes.

## helper.py logic
Contains simple functions to make scripts shorter:
1. wait_and_click: wait for selector then click
2. wait_and_type: wait for selector then clear and type
3. select_option: wait for select dropdown then choose
4. scroll_down: scroll to bottom of page
5. get_random_val: returns random string number between min and max
