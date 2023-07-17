import os
import re
from time import sleep
from datetime import datetime, timedelta
from RPA.Browser.Selenium import Selenium
from constants import (
    BREADCRUMB_BUTTON,
    CATEGORY_SECTION,
    CATEGORY_SELECTION,
    DATE_SELECTION,
    MONTHS,
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
        for category in NEWS_CATEGORY:
            match = re.search(category, item.text, re.IGNORECASE)
            if match:
                item.click()
    sleep(4)


def iterate_news(news_selection):
    breakpoint()
    news_response = []
    section_items = browser_lib.get_webelements(news_selection)
    for li_element in section_items:
        div_element_1 = li_element.find_element("xpath", './/div[@class="css-1bdu3ax"]')
        date_span_element = div_element_1.find_element(
            "xpath", './/span[@class="css-17ubb9w"]'
        )
        div_element_2 = div_element_1.find_element(
            "xpath", './/div[@class="css-1i8vfl5"]'
        )
        div_element_3 = div_element_2.find_element(
            "xpath", './/div[@class="css-e1lvw9"]'
        )

        figure_element = div_element_2.find_element(
            "xpath", './/figure[@class="css-tap2ym"]'
        )
        div = figure_element.find_element("xpath", ".//div")

        title_h4_element = div_element_3.find_element(
            "xpath", '//h4[@class="css-2fgx4k"]'
        )
        description_p_element = div_element_3.find_element(
            "xpath", '//p[@class="css-16nhkrn"]'
        )
        image_element = div.find_element("xpath", '//img[@class="css-rq4mmj"]')

        # Get the value of the src attribute
        src_value = image_element.get_attribute("src")

        news_date = date_span_element.text
        news_title = title_h4_element.text
        news_description = description_p_element.text
        picture_filename = os.path.splitext(os.path.basename(src_value))[0]
        title_count = news_title.count(SEARCH_PHRASE)
        description_count = news_description.count(SEARCH_PHRASE)
        phrase_count = title_count + description_count

        # Define the regex pattern for matching money amounts
        money_pattern = r"\$[\d,]+(\.\d+)?|\d+(\.\d+)? dollars|\d+(\.\d+)? USD"

        # Check if the title contains any amount of money
        title_has_money = bool(re.search(money_pattern, news_title))

        # Check if the description contains any amount of money
        description_has_money = bool(re.search(money_pattern, news_description))

        # Check if either title or description has money
        has_money = title_has_money or description_has_money
    sleep(4)


def select_dates(months):
    today = datetime.today().strftime("%m/%d/%Y")

    section_items = browser_lib.get_webelements("class:css-guqk22")
    for li_element in section_items:
        button_element = li_element.find_element("tag name", "button")
        button_value = button_element.get_attribute("value")
        if months in [0, 1] and button_value == "Past Month":
            button_element.click()
        if months == 2 and button_value == "Specific Dates":
            two_months_ago = (datetime.today() - timedelta(days=60)).strftime(
                "%m/%d/%Y"
            )
            button_element.click()
            input_elements = browser_lib.get_webelements("class:css-9wn7z1")
            input_elements[0].send_keys(two_months_ago)
            input_elements[1].send_keys(today)
            # Press the Enter key by sending the Keys.RETURN constant
            browser_lib.press_keys(input_elements[1], "\ue007")
        # Print the dates
        if months == 3 and button_value == "Specific Dates":
            three_months_ago = (datetime.today() - timedelta(days=90)).strftime(
                "%m/%d/%Y"
            )
            button_element.click()
            input_elements = browser_lib.get_webelements("class:css-9wn7z1")
            input_elements[0].send_keys(three_months_ago)
            input_elements[1].send_keys(today)
            # Press Enter key
            browser_lib.press_keys(input_elements[1], "\ue007")


def close_browser():
    browser_lib.close_browser()


def main():
    """Start main function for RPA for news search"""
    open_the_website(NYTIMES_URL)
    click(BREADCRUMB_BUTTON)
    type_search(SEARCH_PHRASE)
    click(CATEGORY_SELECTION)
    select_categories(CATEGORY_SECTION)
    click(DATE_SELECTION)
    breakpoint()
    select_dates(MONTHS)
    sleep(4)
    iterate_news(NEWS_SELECTION)


if __name__ == "__main__":
    try:
        main()
    finally:
        close_browser()
