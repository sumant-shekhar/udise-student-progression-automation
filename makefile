.PHONY: setup install install-browsers run-app run-bot find-xpaths clean help

# ── Variables ──────────────────────────────────────────────
PYTHON = python3

# ── Setup ──────────────────────────────────────────────────
setup: install install-browsers
	@echo "Setup complete. Run 'make run-app' to start."

install:
	pip install -r requirements.txt

install-browsers:
	playwright install chromium

install-ocr:
	pip install pytesseract pillow
	@echo "Also install tesseract: sudo apt install tesseract-ocr"

# ── Run ────────────────────────────────────────────────────
run-app:
	$(PYTHON) app.py

run-bot:
	$(PYTHON) progression_bot.py

find-xpaths:
	$(PYTHON) get_xpaths.py

# ── Clean ──────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

# ── Help ───────────────────────────────────────────────────
help:
	@echo ""
	@echo "UDISE Automation — available commands:"
	@echo ""
	@echo "  make setup          Install everything needed to run"
	@echo "  make run-app        Run student profile entry bot"
	@echo "  make run-bot        Run promotion/progression bot"
	@echo "  make find-xpaths    Run xpath finder (click buttons in browser)"
	@echo "  make install-ocr    Install captcha solver dependencies"
	@echo "  make clean          Remove Python cache files"
	@echo ""
