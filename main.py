from RPA.Browser.Selenium import Selenium

browser_lib = Selenium()


def open_the_website(url):
    """Function printing python version."""
    browser_lib.open_available_browser(url)


def search_for(term):
    """Function printing python version."""
    input_field = "css:input"
    browser_lib.input_text(input_field, term)
    browser_lib.press_keys(input_field, "ENTER")


def store_screenshot(filename):
    """Function printing python version."""
    browser_lib.screenshot(filename=filename)


# Define a main() function that calls the other functions in order:
def main():
    """Function printing python version."""
    try:
        open_the_website("https://robocorp.com/docs/")
        search_for("python")
        store_screenshot("output/screenshot.png")
    finally:
        browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()
