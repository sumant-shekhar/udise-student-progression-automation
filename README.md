# Student Progression Bot

this bot helps to fill student data on udise plus website automatically. i made this because doing it manually takes too much time.

## how to use

1. install python
2. install playwright: `pip install playwright`
3. install browsers: `playwright install chromium`
4. edit the username and password in `app.py` or `progression_bot.py`
5. run it: `python app.py`

## files
- `app.py`: for student profile entry
- `progression_bot.py`: for student promotion/progression
- `helper.py`: contains common functions to click and type

## note
- you need to solve the captcha manually when the browser opens. i added 15 seconds wait for that.
- make sure you are on the right page before pressing enter in the console.
