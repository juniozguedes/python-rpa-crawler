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
)
from schemas import NewsRequest


class NyScrapper:
    def __init__(self):
        self.browser = Selenium()

    def open_the_website(self, url):
        self.browser.open_available_browser(url)

    def click(self, locator):
        self.browser.click_element_when_visible(locator)

    def click_breadcrumb(self, locator, search_phrase):
        """Check if the self.browser is fullscreen or not by
        selecting the correct button"""
        try:
            self.browser.click_element_when_visible(locator)
            self.type_search(search_phrase)
        except AssertionError:
            print("self.browser detected fullscreen activity")
            self.click_button_with_class("css-tkwi90")
            self.type_search(search_phrase)

    def type_search(self, search_phrase):
        search_input = "name:query"
        self.browser.input_text(search_input, search_phrase)
        self.browser.press_keys(search_input, "ENTER")

    def select_categories(self, category_section, NEWS_CATEGORY):
        """Select and match categories from NEWS_CATEGORY input WorkItem
        params:
        category_section: the css locator for the categories
        NEWS_CATEGORY: WorkInput declaring the categories eg.: ["Sports"]

        """
        section_items = self.browser.get_webelements(category_section)
        for item in section_items:
            for category in NEWS_CATEGORY:
                match = re.search(category, item.text, re.IGNORECASE)
                if match:
                    item.click()
        sleep(2)

    def clean_filename(self, filename):
        # Remove any invalid characters from the filename
        return re.sub(r"[^a-zA-Z0-9_-]", "", filename)

    def load_more_news(self):
        """Checks if there is the ~load more~ button on the bottom"""
        while True:
            load_more_button = self.browser.get_webelements("class:css-vsuiox")
            if not load_more_button:
                # If no "Load More" button is found, break out of the loop
                break

            # Click on the first "Load More" button
            button_element = load_more_button[0].find_element("xpath", ".//button")
            button_element.click()

            # Wait for a short time to allow more news to load
            time.sleep(2)

    def get_post_description(self, element):
        """Get the body of the post
        params:
        element: webdriver element containing p
        """
        try:
            description_p_element = element.find_element(
                "xpath", './/p[@class="css-16nhkrn"]'
            )
            return description_p_element.text
        except NoSuchElementException:
            return "Error: Description not found"

    def get_post_title(self, element):
        """Get the title of the post
        params:
        element: webdriver element containing h4
        """
        try:
            title_h4_element = element.find_element(
                "xpath", './/h4[@class="css-2fgx4k"]'
            )
            return title_h4_element.text
        except NoSuchElementException:
            return "Error: Title not found"

    def iterate_news(self, news_selection, SEARCH_PHRASE):
        """Loops through all news posts saving the excel and images
        params:
        news_selection: The class locator containing the div of posts
        SEARCH_PHRASE: WorkItem input for searching the news by string
        """
        # If you don't wish to load and save ALL news from all pages, comment below
        self.load_more_news()
        news_response = []
        section_items = self.browser.get_webelements(news_selection)
        for li_element in section_items:
            # Navigate through necessary divs for post handling (div 1,2,3)
            date_span_element = li_element.find_element(
                "xpath", ".//span[@class='css-17ubb9w']"
            )
            div_element_1 = li_element.find_element(
                "xpath", ".//div[@class='css-1i8vfl5']"
            )
            div_element_2 = div_element_1.find_element(
                "xpath", ".//div[@class='css-e1lvw9']"
            )

            # Try to get and handle the image part by retrieving the figure
            try:
                figure_element = div_element_1.find_element(
                    "xpath", ".//figure[@class='css-tap2ym']"
                )
                div = figure_element.find_element("xpath", ".//div")

                image_element = div.find_element("xpath", './/img[@class="css-rq4mmj"]')
                # Get the value of the src attribute
                src_value = image_element.get_attribute("src")
                picture_filename = os.path.splitext(os.path.basename(src_value))[0]
                # Clean the picture filename
                picture_filename = self.clean_filename(picture_filename)
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

                # Write the image to the file
                image_path = os.path.join(
                    image_dir, f"{picture_filename}{image_extension}"
                )
                with open(image_path, "wb") as f:
                    f.write(image_response.content)
            except NoSuchElementException:
                src_value = "NA"
                picture_filename = "NA"

            news_title = self.get_post_title(div_element_2)
            news_description = self.get_post_description(div_element_2)

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
        excel_file_path = os.path.join(
            f"{project_root}/src/{SEARCH_PHRASE}", "news.xlsx"
        )

        # Save the DataFrame to an Excel file
        df.to_excel(excel_file_path, index=False)

        return True

    def select_dates(self, months):
        today = datetime.today().strftime("%m/%d/%Y")

        section_items = self.browser.get_webelements("class:css-guqk22")
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
                input_elements = self.browser.get_webelements("class:css-9wn7z1")
                input_elements[0].send_keys(two_months_ago)
                input_elements[1].send_keys(today)
                # Press the Enter key by sending the Keys.RETURN constant
                self.browser.press_keys(input_elements[1], "\ue007")
                break

            # Print the dates
            if months == 3 and button_value == "Specific Dates":
                three_months_ago = (datetime.today() - timedelta(days=90)).strftime(
                    "%m/%d/%Y"
                )
                button_element.click()
                input_elements = self.browser.get_webelements("class:css-9wn7z1")
                input_elements[0].send_keys(three_months_ago)
                input_elements[1].send_keys(today)
                # Press Enter key
                self.browser.press_keys(input_elements[1], "\ue007")
                break

    def close_browser(self):
        self.browser.close_browser()

    def click_button_with_class(self, class_name):
        try:
            button_element = self.browser.get_webelement("class:" + class_name)
            button_element.click()
        except NoSuchElementException:
            print(f"Button with class '{class_name}' not found.")

    def setup(self, request: NewsRequest):
        """Orchestrate robot functions"""
        self.open_the_website(NYTIMES_URL)
        # Reject cookies
        self.click_button_with_class("css-aovwtd")
        # Click on breadcrumb and check if it's fullscreen or not
        self.click_breadcrumb(BREADCRUMB_BUTTON, request.search_phrase)
        # Select category if there is any
        if request.news_category:
            self.click(CATEGORY_SELECTION)
            self.select_categories(CATEGORY_SECTION, request.news_category)
        # Handle dates
        self.click(DATE_SELECTION)
        self.select_dates(request.months)
        sleep(4)
        # Check if iterate news returns success
        if self.iterate_news(NEWS_SELECTION, request.search_phrase):
            print("Script ran successfuly")
            return True
        print("Error iterating news")
        return False
