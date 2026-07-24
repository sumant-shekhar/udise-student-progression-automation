# Student Progression Bot

A small local automation script for Udise student progression and profile entry. This is an old repo for a friend and not actively maintained.

## Quick Start

1. Install dependencies:

```bash
make setup
```

If you do not want to use the helper, you can still install manually:

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

2. Edit your credentials in `app.py` or `progression_bot.py`.

3. Run the script you need:

```bash
make run-app
# or
make run-bot
```

If you do not want to use `make`, you can also run them directly:

```bash
.venv/bin/python app.py
.venv/bin/python progression_bot.py
```

## Files
- `app.py`: update student profile sections (GP, EP, FP, PP)
- `progression_bot.py`: update promotion/progression rows
- `helper.py`: shared browser helper functions
- `get_xpaths.py`: tool to locate element xpaths
- `captcha_sol.py`: optional captcha solving helper

## Notes
- The script waits for captcha before continuing.
- Press ENTER only when you are on the correct page.
- This repo is old and was used locally; keep that in mind.
