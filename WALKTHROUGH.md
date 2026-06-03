# Project Walkthrough

## File Descriptions

*   `app.py`: Acts as the main entry point for the automation tasks.
*   `captcha_sol.py`: Contains the logic used for solving CAPTCHAs.
*   `get_xpaths.py`: Manages the XPath selectors for the web elements on the target site.
*   `helper.py`: Provides utility functions shared across the automation scripts.
*   `progression_bot.py`: Executes the specific logic for student progression.
*   `requirements.txt`: Lists all necessary Python dependencies for the project.

## Running GP/EP (app.py)

This script automates the login and data update process on the UDISE+ portal.

1.  **Preparation**:
    *   Set up your virtual environment and install dependencies: `pip install -r requirements.txt`.
    *   Update the `USERNAME` and `PASSWORD` variables in `app.py`.

2.  **Execution and Automation Flow**:
    *   Run the script with: `python app.py`.
    *   **Login Flow (`login` function)**:
        *   The script launches a browser and navigates to the login page.
        *   It automatically fills in your credentials using the `helper.wait_and_type` function (lines 16-18).
        *   It then triggers an automated attempt to solve the CAPTCHA via `captcha_sol.solve_captcha` (line 21).
        *   **CAPTCHA Verification (lines 23-24)**: The script enters a 15-second sleep (`time.sleep(15)`). This is intended for you to manually verify that the automatically entered CAPTCHA is correct. If it is wrong, you have this time to manually correct it.
        *   After the 15-second pause, the script attempts to automatically click the login button (lines 27-41).
    *   **Post-Login**:
        *   Once the login is successful, the script pauses again, waiting for you to press Enter in the terminal to confirm you are on the student list page.
        *   It then proceeds to loop through students, performing the General, Enrolment, and Facility profile updates, and finally completing the data preview for each student automatically.

## Running Progression Automation

This script automates the student progression status updates.

1.  **Preparation**:
    *   Ensure dependencies are installed: `pip install -r requirements.txt`.
    *   Update `USER` and `PASS` in `progression_bot.py`.

2.  **Execution and Automation Flow**:
    *   Run the script with: `python progression_bot.py`.
    *   **Login Flow (`login` function)**:
        *   Navigates to the login page and enters credentials using `helper.wait_and_type`.
        *   **CAPTCHA Pause**: Similar to `app.py`, it pauses for 15 seconds (`time.sleep(15)`) to allow manual CAPTCHA verification before attempting to log in.
        *   Prompts you to press Enter in the terminal once you are on the dashboard.
    *   **Processing Students (`process_student_row` function)**:
        The core of the progression automation is handled by the `process_student_row(page, row_num)` function. It iterates through table rows (1-100) and performs the following for each student:

        1.  **Locates the Row**: It dynamically constructs an XPath selector (`base_xpath`) using the provided `row_num` to target the specific table row in the DOM.
        2.  **Sets Progression Status**: Finds the status dropdown (`/td[3]/select`) and sets it to "Promoted" (value "1").
        3.  **Enters Marks**: Generates a random integer between 60 and 95 and enters it into the marks input field (`/td[4]/input`).
        4.  **Enters Attendance**: Generates a random integer between 200 and 220 and enters it into the attendance days input field (`/td[5]/input`).
        5.  **Sets Schooling Status**: Finds the schooling status dropdown (`/td[6]/select`) and sets it to "Studying in same school" (value "1").
        6.  **Clicks Update**: Locates the action button for that specific row (`/td[8]/button`) and clicks it to submit the changes.
        7.  **Error Handling**: If any step fails (e.g., the element is not found, or the page is unresponsive), the function catches the exception, prints an error message, and returns `False`. If successful, it returns `True`.

        *Note: The XPath used for `base_xpath` is hardcoded. If the structure of the UDISE+ website changes, this XPath will need to be updated.*
