import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # we start browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        # this javascript will find the xpath when you click
        js_code = """
        window.onclick = function(e) {
            let el = e.target;
            
            function getDynamicXPath(element) {
                // 1. try ID
                if (element.id) return `//*[@id="${element.id}"]`;
                
                // 2. try Name
                if (element.name) return `//*[@name="${element.name}"]`;
                
                // 3. try Text for buttons/links
                let text = element.innerText ? element.innerText.trim() : "";
                if (text && text.length < 50) {
                    if (element.tagName === 'BUTTON' || element.tagName === 'A' || element.tagName === 'SPAN') {
                        return `//${element.tagName}[normalize-space(text())='${text}']`;
                    }
                }
                
                // 4. fall back to simple path
                let path = '';
                while (element && element.nodeType === 1) {
                    let tag = element.tagName.toLowerCase();
                    let siblings = Array.from(element.parentNode.children).filter(c => c.tagName === element.tagName);
                    if (siblings.length > 1) {
                        let index = siblings.indexOf(element) + 1;
                        tag += `[${index}]`;
                    }
                    path = '/' + tag + path;
                    element = element.parentNode;
                }
                return path;
            }
            
            let xpath = getDynamicXPath(el);
            let label = el.innerText || el.value || el.id || el.tagName;
            console.log(`FOUND: ${label.trim()} - ${xpath}`);
            
            // show a red border so you know it worked
            el.style.outline = '2px solid red';
        };
        """
        
        # inject the script
        page.add_init_script(js_code)
        
        print("\n" + "="*50)
        print("XPATH FINDER TOOL")
        print("1. Go to any page in the browser")
        print("2. Click any button or input")
        print("3. Look here to see the dynamic XPath")
        print("="*50 + "\n")
        
        # catch console logs from browser
        def handle_log(msg):
            if "FOUND:" in msg.text:
                print(msg.text)
                with open("found_xpaths.txt", "a") as f:
                    f.write(msg.text.replace("FOUND: ", "") + "\n")
        
        page.on("console", handle_log)
        
        # open the site
        page.goto("https://sdms.udiseplus.gov.in/p0/v1/login?state-id=110")
        
        input("\nPress Enter here to close everything when you are finished...\n")
        browser.close()

if __name__ == "__main__":
    run()
