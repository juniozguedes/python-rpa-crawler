import os
import re
import time
import requests
import pandas as pd
from time import sleep
from urllib.parse import urlparse
from datetime import datetime, timedelta
from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import NoSuchElementException
from constants import (
    BREADCRUMB_BUTTON,
    CATEGORY_SECTION,
    CATEGORY_SELECTION,
    DATE_SELECTION,
    NEWS_SELECTION,
    NYTIMES_URL,
    SEARCH_BUTTON,
)
from schemas import NewsRequest

browser_lib = Selenium()


def open_the_website(url):
    browser_lib.open_available_browser(url)


def click(locator):
    browser_lib.click_element_when_visible(locator)


def click_breadcrumb(locator, search_phrase):
    try:
        browser_lib.click_element_when_visible(locator)
        type_search(search_phrase)
    except AssertionError:
        print("Browser detected fullscreen activity")
        click_button_with_class("css-tkwi90")
        type_search(search_phrase)


def type_search(search_phrase):
    search_input = "name:query"
    browser_lib.input_text(search_input, search_phrase)
    browser_lib.press_keys(search_input, "ENTER")


def select_categories(category_section, NEWS_CATEGORY):
    # Beter work can be done here to replace category for None if NA
    section_items = browser_lib.get_webelements(category_section)
    for item in section_items:
        for category in NEWS_CATEGORY:
            match = re.search(category, item.text, re.IGNORECASE)
            if match:
                item.click()
    sleep(2)


def clean_filename(filename):
    # Remove any invalid characters from the filename
    return re.sub(r"[^a-zA-Z0-9_-]", "", filename)


def load_more_news():
    while True:
        load_more_buttons = browser_lib.get_webelements("class:css-vsuiox")
        if not load_more_buttons:
            # If no "Load More" button is found, break out of the loop
            break

        # Click on the first "Load More" button
        button_element = load_more_buttons[0].find_element("xpath", ".//button")
        button_element.click()

        # Wait for a short time to allow more news to load
        time.sleep(2)


def get_post_description(element):
    try:
        description_p_element = element.find_element(
            "xpath", './/p[@class="css-16nhkrn"]'
        )
        return description_p_element.text
    except NoSuchElementException:
        return "Error: Description not found"


def get_post_title(element):
    try:
        title_h4_element = element.find_element("xpath", './/h4[@class="css-2fgx4k"]')
        return title_h4_element.text
    except NoSuchElementException:
        return "Error: Title not found"


def iterate_news(news_selection, SEARCH_PHRASE):
    # If you don't wish to load and save ALL news from all pages, comment below
    load_more_news()
    news_response = []
    section_items = browser_lib.get_webelements(news_selection)
    for li_element in section_items:
        date_span_element = li_element.find_element(
            "xpath", ".//span[@class='css-17ubb9w']"
        )
        div_element_2 = li_element.find_element("xpath", ".//div[@class='css-1i8vfl5']")
        div_element_3 = div_element_2.find_element(
            "xpath", ".//div[@class='css-e1lvw9']"
        )
        try:
            figure_element = div_element_2.find_element(
                "xpath", ".//figure[@class='css-tap2ym']"
            )
            div = figure_element.find_element("xpath", ".//div")

            image_element = div.find_element("xpath", './/img[@class="css-rq4mmj"]')
            # Get the value of the src attribute
            src_value = image_element.get_attribute("src")
            picture_filename = os.path.splitext(os.path.basename(src_value))[0]
            # Clean the picture filename
            picture_filename = clean_filename(picture_filename)
            # Extract the filename from the URL without query parameters
            parsed_url = urlparse(src_value)
            filename_without_params = os.path.basename(parsed_url.path)
            # Download the image and save it to the "root" folder
            image_url = src_value
            image_response = requests.get(image_url)
            image_extension = os.path.splitext(filename_without_params)[1]
            # Define the directory path for images
            image_dir = os.path.join("src", SEARCH_PHRASE, "img")

            # Create the directory if it doesn't exist
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Now, you can write the image to the file
            image_path = os.path.join(image_dir, f"{picture_filename}{image_extension}")
            with open(image_path, "wb") as f:
                f.write(image_response.content)
        except NoSuchElementException:
            src_value = "NA"
            picture_filename = "NA"

        news_title = get_post_title(div_element_3)
        news_description = get_post_description(div_element_3)

        news_date = date_span_element.text
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
        news_response.append(
            {
                "date": news_date,
                "title": news_title,
                "description": news_description,
                "picture_filename": picture_filename,
                "count_of_search_phrases": phrase_count,
                "has_money": has_money,
            }
        )
    # Get the path of the main.py script
    script_path = os.path.abspath(__file__)

    # Get the project root folder path
    project_root = os.path.dirname(script_path)
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(news_response)

    # Define the Excel file path within the project root folder
    excel_file_path = os.path.join(f"{project_root}/src/{SEARCH_PHRASE}", "news.xlsx")

    # Save the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)

    return True


def select_dates(months):
    today = datetime.today().strftime("%m/%d/%Y")

    section_items = browser_lib.get_webelements("class:css-guqk22")
    for li_element in section_items:
        button_element = li_element.find_element("tag name", "button")
        button_value = button_element.get_attribute("value")
        if months in [0, 1] and button_value == "Past Month":
            button_element.click()
            break
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
            break

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
            break


def close_browser():
    browser_lib.close_browser()


def click_button_with_class(class_name):
    try:
        button_element = browser_lib.get_webelement("class:" + class_name)
        button_element.click()
    except NoSuchElementException:
        print(f"Button with class '{class_name}' not found.")


def setup(request: NewsRequest):
    open_the_website(NYTIMES_URL)
    click_button_with_class("css-aovwtd")
    click_breadcrumb(BREADCRUMB_BUTTON, request.search_phrase)
    if request.news_category:
        click(CATEGORY_SELECTION)
        select_categories(CATEGORY_SECTION, request.news_category)
    click(DATE_SELECTION)
    select_dates(request.months)
    sleep(4)
    if iterate_news(NEWS_SELECTION, request.search_phrase):
        print("Script ran successfuly")
        return True
    print("Error iterating news")
    return False
