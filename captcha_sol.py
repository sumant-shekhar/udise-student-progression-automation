try:
    import pytesseract
    from PIL import Image
    import io
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False
    import io


def solve_captcha(page, image_xpath, input_xpath):
    if not HAS_LIBS:
        print("skipping auto-captcha because pytesseract or pillow is not installed")
        return False
    try:
        print("trying to solve captcha automatically...")
        
        # find the captcha image
        captcha_img = page.locator(f"xpath={image_xpath}")
        
        # take a screenshot of only the captcha
        img_bytes = captcha_img.screenshot()
        
        # load it into PIL
        img = Image.open(io.BytesIO(img_bytes))
        
        # use tesseract to get text
        text = pytesseract.image_to_string(img)
        text = text.strip() # remove spaces
        
        print(f"found captcha text: {text}")
        
        if text:
            # type it into the box
            page.fill(f"xpath={input_xpath}", text)
            return True
        else:
            print("couldnt read any text from captcha")
            return False
            
    except Exception as e:
        print("error solving captcha:", e)
        return False
