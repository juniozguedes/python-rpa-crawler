from RPA.Browser.Selenium import Selenium
from time import sleep

browser_lib = Selenium()


def open_the_website(url):
    browser_lib.open_available_browser(url)


def click_on(input_field):
    browser_lib.wait_until_element_is_visible(input_field, timeout="10s")
    browser_lib.click_element(input_field)


def search_for(term):
    input_field = "data-testid:search-input"
    browser_lib.input_text(input_field, term)
    sleep(1)  # Wait for suggestions or search results to appear


# Define a main() function that calls the other functions in order:
def main():
    """Start main function for RPA for news search
    constant variables:
        NYTIMES_URL : str (new york times URL string)
        SEARCH_PHRASE : str (The desired search phrase)
    """
    try:
        NYTIMES_URL = "https://www.nytimes.com"
        SEARCH_PHRASE = "robbery"

        open_the_website(NYTIMES_URL)
        click_on("desktop-sections-button")
        search_for(SEARCH_PHRASE)
    finally:
        browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()
