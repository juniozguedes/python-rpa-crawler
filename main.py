import re
from time import sleep
from RPA.Browser.Selenium import Selenium
from constants import (
    BREADCRUMB_BUTTON,
    CATEGORY_SECTION,
    CATEGORY_SELECTION,
    NEWS_CATEGORY,
    NEWS_SELECTION,
    NYTIMES_URL,
    SEARCH_BUTTON,
    SEARCH_PHRASE,
)

browser_lib = Selenium()


def open_the_website(url):
    browser_lib.open_available_browser(url)


def click(locator):
    browser_lib.click_element_when_visible(locator)


def type_search(search_phrase):
    search_input = "name:query"
    click(SEARCH_BUTTON)
    browser_lib.input_text(search_input, search_phrase)
    browser_lib.press_keys(search_input, "ENTER")


def select_categories(category_section):
    section_items = browser_lib.get_webelements(category_section)
    for item in section_items:
        print(f"item: {item}")
        print(f"txt: {item.text}")
        for category in NEWS_CATEGORY:
            print(f"{category}, {NEWS_CATEGORY}")
            match = re.search(category, item.text, re.IGNORECASE)
            if match:
                item.click()
    sleep(4)


def iterate_news(news_selection):
    breakpoint()
    section_items = browser_lib.get_webelements(news_selection)
    for item in section_items:
        print(f"item: {item}")
        print(f"txt: {item.text}")
        for category in NEWS_CATEGORY:
            print(f"{category}, {NEWS_CATEGORY}")
            match = re.search(category, item.text, re.IGNORECASE)
            if match:
                item.click()
    sleep(4)


def close_browser():
    browser_lib.close_browser()


def main():
    """Start main function for RPA for news search"""
    breakpoint()
    open_the_website(NYTIMES_URL)
    click(BREADCRUMB_BUTTON)
    type_search(SEARCH_PHRASE)
    click(CATEGORY_SELECTION)
    select_categories(CATEGORY_SECTION)
    sleep(4)
    iterate_news(NEWS_SELECTION)


if __name__ == "__main__":
    try:
        main()
    finally:
        close_browser()
