# UDISE+ Student Progression Automation

## Overview

An enterprise-grade headless automation framework using **Playwright** to handle the annual UDISE+ student data validation and progression workflows. This system automatically cycles through student profiles, updates academic parameters, and confirms data progression with resilient error handling and retry mechanisms.

**Status**: Production-ready | **Framework**: Playwright (Python) | **Version**: 1.0.0

## Architecture

### Core Workflow

```
[Login] → [Dashboard] → [Select Class] 
    ↓
[Detect Students] → [Process Each Student]
    ↓
[Update Marks] → [Update Days] → [Update Status]
    ↓
[Confirm Changes] → [Next Student]
    ↓
[Repeat for Next Class]
```

### Module Structure

```
src/
├── __init__.py                 # Package initialization
├── main.py                     # Main orchestrator and automation loop
├── playwright_utils.py         # Playwright utilities with retry logic
├── progression.py              # Student progression handler
config/
├── settings.py                 # Configuration and environment settings
tests/
├── (test modules - planned)
requirements.txt                # Python dependencies
.env.example                     # Environment template
README.md                        # This file
```

## Key Features

✅ **Resilient Element Interactions**: Automatic retry logic with exponential backoff  
✅ **Network-Aware Waits**: Replaces fragile `time.sleep()` with proper wait conditions  
✅ **Comprehensive Error Handling**: Graceful degradation for non-critical fields  
✅ **Batch Processing**: Continuous loop monitoring for new class selections  
✅ **Execution Logs**: Detailed progress tracking with emoji indicators  
✅ **Screenshot Debugging**: Automatic screenshots on errors  
✅ **Browser Flexibility**: Support for Chromium, Firefox, and WebKit  

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Package manager
- **Browser**: Google Chrome or Chromium installed
- **Network**: Access to UDISE+ platform (https://sdms.udiseplus.gov.in)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/udise-student-progression-automation.git
cd udise-student-progression-automation
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Configure Credentials

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` with your UDISE+ credentials:

```
UDISE_USERNAME=your_username
UDISE_PASSWORD=your_password
HEADLESS=false
BROWSER_TYPE=chromium
```

## Usage

### Basic Execution

```bash
python3 -m src.main
```

### Step-by-Step Workflow

1. **Script Launch**: Browser opens UDISE+ login page
2. **Automatic Login**: Credentials are auto-filled from `.env`
3. **MFA Wait**: 15-second buffer for multi-factor authentication (if enabled)
4. **Dashboard Load**: Script waits for dashboard to fully load
5. **Ready for Input**: Navigate to a class and select it
6. **Automatic Processing**: Script detects students and processes each one:
   - Sets promotion status
   - Enters marks (60-80% random or custom)
   - Enters attendance days (200-220 random or custom)
   - Assigns section
   - Confirms changes
7. **Loop Continuation**: After batch completion, wait 10 seconds for next class selection

### Keyboard Controls

- **Ctrl+C**: Stop automation gracefully
- Displays summary statistics on exit

## Configuration

All settings are managed in `config/settings.py`:

```python
# Timeouts (in milliseconds)
WAIT_TIMEOUT = 15000       # Element visibility timeout
ELEMENT_TIMEOUT = 5000     # General element interaction timeout
NAVIGATION_TIMEOUT = 30000 # Page navigation timeout

# Retry configuration
MAX_RETRIES = 3            # Retry attempts for failed actions
RETRY_DELAY = 0.5          # Delay between retries (seconds)

# Loop settings
LOOP_CHECK_INTERVAL = 10   # Seconds between class checks
```

## API Reference

### PlaywrightUtils

Core utility class for Playwright interactions:

```python
from src.playwright_utils import PlaywrightUtils

utils = PlaywrightUtils(page, base_timeout=5000)

# Safe input with auto-retry
utils.safe_input("id=field", "value")

# Safe click with retries
utils.safe_click("xpath=/path/to/button")

# Select dropdown option
utils.safe_select("xpath=/path/to/select", "option_value")

# Get dropdown options
options = utils.get_select_options("xpath=/path/to/select")

# Element visibility check
if utils.is_visible("xpath=/path/to/element"):
    print("Element found!")
```

### ProgressionHandler

Student progression workflow manager:

```python
from src.progression import ProgressionHandler

handler = ProgressionHandler(page, utils)

# Process single student row
failed_rows = []
handler.process_student_row(row_index=1, failed_rows=failed_rows)

# Set individual fields
handler.set_promotion_status(1)
handler.set_marks(1, marks=75)
handler.set_attendance_days(1, days=210)
handler.set_section(1)
```

## Troubleshooting

### Issue: Login fails with timeout

**Solution**: Check if credentials are correct. Increase `WAIT_TIMEOUT` in settings.py:

```python
WAIT_TIMEOUT = 20000  # Increase to 20 seconds
```

### Issue: Elements not found

**Solution**: School may have updated UI. Update XPath selectors in corresponding module:

```python
# Verify with F12 Developer Tools in browser
# Update xpath in src/progression.py
```

### Issue: Random failures during batch processing

**Solution**: Increase retry settings:

```python
MAX_RETRIES = 5        # Increase attempts
RETRY_DELAY = 1.0      # Increase delay between retries
```

### Debug Mode

Enable screenshots on errors:

```python
# In src/main.py, add before processing:
self.utils.take_screenshot("/tmp/debug.png")
```

## Performance Optimization

### For Faster Execution

1. **Set headless mode** in `.env`:
   ```
   HEADLESS=true
   ```

2. **Reduce wait times** (use cautiously):
   ```python
   WAIT_TIMEOUT = 10000  # Reduce from 15s
   LOOP_CHECK_INTERVAL = 5  # Reduce from 10s
   ```

3. **Use Firefox** (sometimes faster):
   ```
   BROWSER_TYPE=firefox
   ```

### For More Stability

1. **Increase timeouts**:
   ```python
   WAIT_TIMEOUT = 20000
   ELEMENT_TIMEOUT = 7000
   ```

2. **Increase retry delays**:
   ```python
   RETRY_DELAY = 1.0
   MAX_RETRIES = 5
   ```

## Development

### Project Structure Philosophy

- **Separation of Concerns**: Utils, handlers, and orchestration are separate modules
- **Configuration Externalization**: All settings in `config/settings.py`
- **Resilient Interactions**: All element interactions have retry logic and error handling
- **Type Hints**: Full type annotations for IDE support and documentation

### Adding New Workflows

To add new profile handlers (e.g., GP, EP, FP/PP):

1. Create new handler class in `src/profile_handler.py`
2. Inherit common patterns from `ProgressionHandler`
3. Register in `AutomationOrchestrator` in `src/main.py`
4. Update configuration in `config/settings.py` if needed

### Running Tests

```bash
# (Tests planned for next release)
python3 -m pytest tests/
```

## Migration from Selenium

This framework is the Playwright successor to previous Selenium-based automation:

**Key Improvements:**
- ✅ Built-in auto-wait (no manual `time.sleep()`)
- ✅ Better browser support (Chromium, Firefox, WebKit)
- ✅ More reliable element detection
- ✅ Network interception capabilities
- ✅ Easier debugging with browser context

## Security

⚠️ **Important**: Never commit credentials to version control:

1. Always use `.env` file (added to `.gitignore`)
2. Use `.env.example` as template
3. Set environment variables in CI/CD platforms

```bash
# Set via environment
export UDISE_USERNAME="your_username"
export UDISE_PASSWORD="your_password"
python3 -m src.main
```

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support & Contributions

For issues, bugs, or feature requests, please open an issue on GitHub.

## Changelog

### v1.0.0 (2026-06-02)
- Initial release with Playwright migration
- Core progression workflow implementation
- Full error handling and retry logic
- Continuous monitoring loop
- Professional configuration management

---

**Last Updated**: June 2, 2026  
**Maintained by**: Development Team  
**Status**: Active Development

