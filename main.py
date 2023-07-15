from time import sleep
from RPA.Browser.Selenium import Selenium
from constants import (
    BREADCRUMB_BUTTON,
    CATEGORY_SELECTION,
    NEWS_CATEGORY,
    NYTIMES_URL,
    SEARCH_BUTTON,
    SEARCH_PHRASE,
    SECTION_BUTTON,
    SECTION_CATEGORIES,
)

browser_lib = Selenium()


def open_the_website(url):
    browser_lib.open_available_browser(url)


def click(locator):
    browser_lib.click_element_when_visible(locator)


def type_search(locator):
    search_input = "name:query"
    click(SEARCH_BUTTON)
    browser_lib.input_text(search_input, locator)
    browser_lib.press_keys(search_input, "ENTER")


def select_categories():
    browser_lib.click_element_when_visible(SECTION_BUTTON)
    section_items = browser_lib.get_webelements(SECTION_CATEGORIES)
    print(f"section itens: {section_items}")
    for item in section_items:
        print(item)
        for category in NEWS_CATEGORY:
            print(f"{category}, {NEWS_CATEGORY}")
            if category == browser_lib.get_text(item):
                item.click()

    sleep(4)


def close_browser():
    browser_lib.close_browser()


def main():
    """Start main function for RPA for news search"""
    open_the_website(NYTIMES_URL)
    click(BREADCRUMB_BUTTON)
    type_search(SEARCH_PHRASE)
    click(CATEGORY_SELECTION)
    sleep(10)


if __name__ == "__main__":
    try:
        main()
    finally:
        close_browser()
