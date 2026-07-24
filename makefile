.PHONY: setup venv install install-browsers install-ocr run-app run-bot find-xpaths clean help

# ── Variables ──────────────────────────────────────────────
PYTHON ?= python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
PIP = $(VENV_PYTHON) -m pip

# ── Setup ──────────────────────────────────────────────────
setup: venv install install-browsers
	@echo "Setup complete. Run 'make run-app' to start."

venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Created virtual environment at $(VENV)."

install: venv
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

install-browsers: install
	$(VENV_PYTHON) -m playwright install chromium

install-ocr: install
	$(PIP) install pytesseract pillow
	@echo "Also install tesseract: sudo apt install tesseract-ocr"

# ── Run ────────────────────────────────────────────────────
run-app:
	$(VENV_PYTHON) app.py

run-bot:
	$(VENV_PYTHON) progression_bot.py

find-xpaths:
	$(VENV_PYTHON) get_xpaths.py

# ── Clean ──────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

# ── Help ───────────────────────────────────────────────────
help:
	@echo ""
	@echo "UDISE Automation — available commands:"
	@echo ""
	@echo "  make venv             Create a virtual environment"
	@echo "  make install          Install Python dependencies into the venv"
	@echo "  make install-browsers Install Playwright browsers into the venv"
	@echo "  make install-ocr      Install captcha solver dependencies into the venv"
	@echo "  make clean            Remove Python cache files"
	@echo ""
