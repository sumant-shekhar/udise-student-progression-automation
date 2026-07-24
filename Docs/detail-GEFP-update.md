# GEFP Update Script — Walkthrough
    - G = general profile
    - E = enrolment profile
    - F = facility profile
    - p = preview
---

## `update_general_profile(page)` — Step 1: Fix the basic student info

this one's the first of the four student profile updates. it checks the phone number and blood group, fixes them if they're bad, then clicks save and moves to the next step.

**1. checks the phone number**

it looks at what's currently in the phone field. if it's one of those fake test numbers (9999999991, 9999999999) or it's totally empty, it generates a random real-looking phone number and types it in.

**2. scrolls down the page**

just scrolls so you can see more stuff if you're watching.

**3. checks the blood group dropdown**

looks at the blood group field. if nothing's selected (empty), it picks "9" which means "unknown".

**4. clicks the Save button**

finds the save button and smacks it. waits a tiny bit.

**5. clicks OK on the popup alert**

when you click save it shows a confirmation popup. the script clicks the yes/ok button on it. waits a tiny bit.

**6. clicks Next to go to step 2**

finds the next button and clicks it. now you're on the enrolment profile step.

**if something breaks**

the script catches errors and just prints "error in step 1:" plus whatever went wrong. then it bails out.

---

## `update_enrolment_profile(page)` — Step 2: The lazy one

this one doesn't really do anything fancy. it just scrolls, clicks save, confirms, and moves on.

**1. scrolls down**

just scrolls to show more of the form.

**2. clicks Save**

hits the save button without changing anything (this step apparently has no required edits).

**3. clicks OK on the popup**

confirms the save popup that appears.

**4. clicks Next**

moves to step 3 (facility profile).

**if something breaks**

same deal - prints the error and stops.

---

## `update_facility_profile(page)` — Step 3: Same as step 2

literally the exact same thing as enrolment profile. scroll, save, confirm, next.

**1. scrolls down**

scrolls the page.

**2. clicks Save**

clicks save without changing anything.

**3. clicks OK on the popup**

confirms the popup.

**4. clicks Next**

moves to the final step (preview/complete).

**if something breaks**

prints error and stops.

---

## `complete_preview(page)` — Step 4: The final boss

this is the last step. it clicks "Complete Data" twice and you're done with that student. the script says "student done!" when it finishes.

**1. scrolls down**

scrolls to see everything.

**2. clicks the "Complete Data" button**

finds and clicks the button that actually submits all the data.

**3. clicks OK on the first popup**

confirms the popup that shows up.

**4. clicks OK on the second popup**

has to confirm again for some reason (double confirm - sites be like that sometimes).

**5. prints "student done!"**

congrats! one student is finished.

**6. moves to the next student automatically**

the main script handles finding the next student button, this function just finishes one student.

**if something breaks**

prints error and stops.

---