from time import sleep
from RPA.Browser.Selenium import Selenium
from constants import BREADCUMB_BUTTON, NYTIMES_URL, SEARCH_BUTTON, SEARCH_PHRASE

browser_lib = Selenium()


def open_the_website(url):
    browser_lib.open_available_browser(url)


def click():
    browser_lib.click_element_when_visible(BREADCUMB_BUTTON)


def search_for():
    search_input = "name:query"
    browser_lib.click_element_when_visible(SEARCH_BUTTON)
    browser_lib.input_text(search_input, SEARCH_PHRASE)
    browser_lib.press_keys(search_input, "ENTER")
    sleep(1)  # Wait for suggestions or search results to appear


def close_browser(self) -> None:
    browser_lib.close_browser()


def main():
    """Start main function for RPA for news search"""
    open_the_website(NYTIMES_URL)
    sleep(4)
    click()
    search_for()


if __name__ == "__main__":
    main()
