# Student Profile Handlers (EP/GP/FP/PP)

Playwright-based student profile automation handlers migrated from the original Selenium code. Each handler manages a specific step in the student profile completion workflow.

## Overview

The profile handlers are part of the UDISE+ Student Progression Automation system that automates the complete student profile update process across four stages:

| Handler | Module | Purpose |
|---------|--------|---------|
| **GP** | `profiles_gp_handler.py` | General Profile - Phone number & blood group |
| **EP** | `profiles_ep_handler.py` | Enrolment Profile - Admission & languages |
| **FP** | `profiles_fp_handler.py` | Facility Profile - Health & facility data |
| **PP** | `profiles_pp_handler.py` | Profile Preview - Final review & submission |

## Architecture

### Module Structure

```
src/
├── profiles_main.py                 # Main orchestrator
├── profiles_playwright_utils.py     # Playwright utilities wrapper
├── profiles_gp_handler.py           # General Profile handler
├── profiles_ep_handler.py           # Enrolment Profile handler
├── profiles_fp_handler.py           # Facility Profile handler
├── profiles_pp_handler.py           # Profile Preview handler
└── profiles_scraper.py              # Student information scraper
```

### Key Components

#### 1. **ProfilePlaywrightUtils** (`profiles_playwright_utils.py`)

Resilient Playwright wrapper providing stable element interactions with retry logic.

**Key Methods:**
- `safe_js(xpath, script, retries=3)` - Execute JavaScript on element
- `safe_input(xpath, value, retries=3)` - Fill input field with clear
- `js_click(xpath, retries=3)` - Click element via JavaScript
- `js_click_css(css, retries=3)` - Click by CSS selector
- `select_by_value(css, value)` - Dropdown selection by value
- `get_input_value(xpath)` - Get input field value
- `scroll_to_bottom()` - Scroll page
- `wait_for_element(xpath)` - Wait for element presence
- `element_exists(xpath)` - Check element existence

**Features:**
- Automatic retry on timeout/errors
- Stale element recovery
- JavaScript fallback for clicks
- XPath/CSS selector support

#### 2. **GeneralProfileUpdater** (`profiles_gp_handler.py`)

Updates general student information.

**Steps:**
1. Generate/validate phone number (format: 97855XXXXX)
2. Select blood group from dropdown
3. Save changes
4. Proceed to next step

**XPath Selectors:**
- Phone input: `//input[@id='phoneNo']`
- Blood group: `select[formcontrolname='bloodGroup']`
- Save button: `//button[normalize-space(span/text())='Save']`

#### 3. **EnrolmentProfileUpdater** (`profiles_ep_handler.py`)

Updates enrolment details and subject selection.

**Steps:**
1. Fill admission number (random 10-99)
2. Select medium of instruction (default: 4-Hindi)
3. Select language group (English/Hindi/Sanskrit)
4. Handle RTE 12C checkbox
5. Select academic subjects based on stream
6. Save and proceed

**Key Features:**
- Subject selection logic based on academic stream
- Multi-select dropdown handling
- Language group fallback options
- XPath preserved for complex selectors

#### 4. **FacilityProfileUpdater** (`profiles_fp_handler.py`)

Updates facility and health-related information.

**Steps:**
1. Select facility provision (Yes)
2. Check textbook availability
3. Set CWSN status
4. Configure disability/special program options:
   - Screened for SLD
   - Autism Spectrum Disorder
   - ADHD (Attention Deficit Hyperactive Disorder)
   - Gifted Children
   - Olympics/NLC
   - NCC/NSS
5. Update height/weight based on class standards
6. Save and proceed

**Class Data Standards:**
Height and weight standards are mapped by class (1-10):
- Class 1: 115cm, 21kg
- Class 5: 138cm, 32kg
- Class 10: 170cm, 56kg

#### 5. **ProfilePreviewComplete** (`profiles_pp_handler.py`)

Handles final profile review and submission.

**Steps:**
1. Review complete profile summary
2. Scroll through all sections
3. Submit profile
4. Confirm SweetAlert2 dialog
5. Navigate to next student or exit

**Features:**
- Profile data extraction
- Alternative button detection (Submit/Complete/Finish)
- Next student navigation
- Session completion handling

#### 6. **StudentInfoScraper** (`profiles_scraper.py`)

Extracts student information from the dashboard.

**Features:**
- Parse student cards from DOM
- Extract name, roll number, class
- Count students in queue
- Batch student extraction

## Usage

### Running the Orchestrator

```bash
# Basic usage
python3 -m src.profiles_main

# With environment variables
export UDISE_USERNAME="your_username"
export UDISE_PASSWORD="your_password"
python3 -m src.profiles_main
```

### Configuration

Create a `.env` file with credentials:

```
UDISE_USERNAME=10140615303
UDISE_PASSWORD=your_password
```

### Programmatic Usage

```python
from playwright.sync_api import sync_playwright
from src.profiles_main import ProfileAutomationOrchestrator

# Initialize
orchestrator = ProfileAutomationOrchestrator(
    username="your_username",
    password="your_password",
    headless=False,
    browser_type="chromium"
)

# Setup browser
orchestrator.setup_browser()

# Login
if orchestrator.login():
    # Process students
    orchestrator.run_automation_loop(max_students=10)

# Cleanup
orchestrator.close_browser()
```

## XPath Selectors (Preserved from Original)

All XPath and CSS selectors from the original Selenium code are preserved:

### General Profile
```
Phone input:     //input[@id='phoneNo']
Blood group:     select[formcontrolname='bloodGroup']
Save button:     //button[normalize-space(span/text())='Save']
```

### Enrolment Profile
```
Admission:       //input[@id='admNo']
Medium:          select[id='medium']
Language:        select[id='languageGroup']
Stream:          //select[@formcontrolname='academicStream']
Subject dropdown://ng-multiselect-dropdown[@formcontrolname='subjectGroup']
RTE 12C:         /html/body/.../form/div[1]/div/div/div[10]/div/div[2]/div[2]/input
```

### Facility Profile
```
Facility YES:    //input[@type='radio' and @formcontrolname='facProvYN' and @value='1']
Textbook:        //input[@type='checkbox' and @id='textbook']
CWSN:            input[formcontrolname='cwsnYN'][value='2']
SLD Screened:    //input[@formcontrolname='screenedForSld' and @value='2']
Height:          //input[@id='height']
Weight:          //input[@id='weight']
```

### Profile Preview
```
Submit:          //button[normalize-space(span/text())='Submit']
Next Student:    //button[normalize-space(text())='Next Student']
Confirm:         div.swal2-actions > button.swal2-confirm
```

## Error Handling

All handlers include comprehensive error handling:

- **Retry Logic**: Automatic retries (3 attempts by default)
- **Graceful Degradation**: Non-critical fields fail without stopping workflow
- **Timeout Handling**: 20-second default wait for elements
- **Stale Element Recovery**: Automatic recovery from stale element references
- **Logging**: Emoji indicators for status (✅ ❌ ⚠️ ℹ️)

## Migration Notes

### From Selenium to Playwright

| Selenium | Playwright |
|----------|-----------|
| `WebDriver` | `Page` |
| `WebDriverWait` | `page.wait_for_*()` |
| `expected_conditions` | Selector-based waits |
| `By.XPATH` | `page.locator(f"xpath={xpath}")` |
| `By.CSS_SELECTOR` | `page.locator(css)` |
| `send_keys()` | `fill()` |
| `clear()` + `send_keys()` | `fill(value)` with auto-clear |
| `Select()` class | `select_option()` method |
| `execute_script()` | `evaluate()` |
| Time-based waits | Auto-wait on actions |

### Preserved Selectors

**All XPath and CSS selectors are kept exactly as in original code**, ensuring compatibility and maintainability.

## Statistics & Logging

Session statistics are tracked:

```
📊 AUTOMATION SESSION STATISTICS
============================================================
Students Processed: 25
Successful: 24
Failed: 1
Duration: 0:15:30
Success Rate: 96.0%
============================================================
```

## Performance Considerations

- **Wait Timeout**: 20 seconds (configurable)
- **Retry Attempts**: 3 per operation
- **Scroll Delay**: 0.2-0.3 seconds
- **Action Delays**: 0.15-0.5 seconds between operations
- **Headless Mode**: Optional (set to `True` for CI/CD)

## Troubleshooting

### Element Not Found
- Increase `wait_timeout` in `ProfilePlaywrightUtils`
- Verify XPath selector accuracy
- Check page load completion

### Stale Element
- Automatically retried (built-in recovery)
- If persistent, check page navigation timing

### CAPTCHA
- Manual intervention required (20-second wait)
- Cannot be automated for security reasons

### Dropdown Not Responding
- Try JavaScript click: `js_click(xpath)`
- Check dropdown framework (Angular/React/etc.)

## Future Enhancements

- [ ] Multi-browser parallel processing
- [ ] Database logging of student updates
- [ ] Advanced error recovery strategies
- [ ] Performance profiling
- [ ] API integration for batch imports

## Support

For issues or questions:
1. Check error messages and logs
2. Verify XPath selectors in browser DevTools
3. Review Playwright documentation
4. Check issue tracker in repository

---

**Last Updated**: June 2, 2026  
**Status**: Production Ready ✅  
**Framework**: Playwright 1.42.1+  
**Python**: 3.8+
