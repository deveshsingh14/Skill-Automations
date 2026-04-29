from playwright.sync_api import sync_playwright
import time

def auto_type_monkeytype():
    with sync_playwright() as p:
        # Launch Chrome. headless=False means you can physically watch it happen!
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Go to the website
        page.goto("https://monkeytype.com/")

        # Give yourself 5 seconds to click "Accept All" on the cookie pop-up 
        # and ensure the typing area is ready.
        print("Waiting 5 seconds for page to load and cookies to be accepted...")
        time.sleep(5)
        print("Starting the typing automation!")

        # 2. Start the infinite typing loop
        while True:
            # Check if the test is over by looking for the hidden typing input to disappear 
            # or the results page to appear.
            if page.locator("#resultWordsHistory").is_visible():
                print("Test finished! Look at that speed.")
                break

            try:
                # Find the currently active word
                active_word = page.locator(".word.active")
                
                # Extract the text inside it
                word_to_type = active_word.inner_text()

                if word_to_type:
                    # 3. Type the word and add a space at the end to move to the next word
                    # 'delay' adds a tiny pause (in milliseconds) between keystrokes.
                    page.keyboard.type(word_to_type + " ", delay=15)
                    
            except Exception:
                # If it briefly can't find a word (e.g., page loading or ending), just pass
                pass

        # Keep the browser open for 10 seconds so you can see your final score
        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    auto_type_monkeytype()