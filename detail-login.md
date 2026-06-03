# login function — Walkthrough

---

## `login(page)` — Getting into UDISE+

ok so this is where it all starts. the script wakes up, opens the browser, throws your username and password at the login page, deals with that annoying captcha thing, and then basically just... waits for you to tell it "yep we're logged in, go ahead now"

---

### what actually happens here

**1. Browser pops open and goes to the login page**

coolest part? you don't do anything. the script just opens the browser window and navigates to `https://sdms.udiseplus.gov.in/p0/v1/login?state-id=110` on its own. just sit back and watch it happen lol

**2. types your username**

script finds that username field (the one with `id="username-field"`) and types in the username. it's using this helper function that waits for the field to actually show up before typing, so it won't rage-type into nothing if the page is being slow

**3. types your password**

same deal but for the password field (`id="password-field"`)

**4. tries to auto-solve the captcha**

here's where it gets spicy. the script runs `captcha_sol.solve_captcha()` which looks at the captcha image (`id="captchaImage"`), tries to figure out what it says, and types the answer into the captcha field (`id="captcha"`). 

will it work? maybe. probably not lol. captchas are annoying for a reason

**5. takes a 15 second nap**

the script just... waits. 15 seconds. why? because if the auto captcha solver messed up (which is likely), you can eyeball it and type it in manually during this time. keep your eyes on the browser window

**6. tries to click the login button**

now it goes hunting for the login button. it tries like 4 different ways to find it:

- looks for an element with `id="submit-btn"` that's a button
- looks for an element with `id="submit-btn"` that's an input 
- looks for any button with the word "Login" in it
- tries some fancy text matching idk

it clicks whichever one it finds first. if literally none of them work it just shrugs and says "couldn't click it myself, you click it"

**7. waits for you to press Enter**

this is the safety net. the script prints:

```
press enter AFTER you are on the student list page...
```

and then just... stops. waiting. it won't do ANYTHING until you press Enter in the terminal. this is so you can make sure you're actually logged in and on the right page before the script starts messing with student data

---

### okay so something broke what do i do

**the captcha solver didn't work / captcha looks wrong**

no stress. you got 15 seconds. just look at your browser, read the captcha, type it in manually. the script is literally waiting for you to do this. after those 15 seconds are up it'll try clicking login

**the login button didn't get clicked**

you'll see this in the terminal:

```
couldnt click login button automatically, please click it yourself if needed
```

cool so just... click the button yourself in the browser. the script is still chilling waiting for your Enter press. you haven't broken anything

**page has an error / won't load / shows something weird**

DO NOT PRESS ENTER YET. fix it first. maybe the captcha was wrong, maybe the password is bad, maybe the site is being weird. log in correctly, get yourself to the student list page, THEN press Enter

**wait the username/password is wrong**

the script uses the `USERNAME` and `PASSWORD` variables at the top of `app.py`. make sure you have updated them with your own credentials before running the script.

**browser just closed for no reason**

yeah the script crashed before it got to the waiting part. check your terminal for an error message. probably something broke in the login page structure (like they changed the HTML IDs or something dumb happened)

---