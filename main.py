import ast
from crawler import close_browser, setup
import configparser

from schemas import NewsRequest


def initialize_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def main():
    """Start main function for RPA for news search"""
    # Initialize the configuration
    config = initialize_config()

    # Accessing values from the configuration
    SEARCH_PHRASE = config.get("General", "SEARCH_PHRASE")
    NEWS_CATEGORY = config.get("General", "NEWS_CATEGORY")
    NEWS_CATEGORY = ast.literal_eval(NEWS_CATEGORY)
    MONTHS = config.getint("General", "MONTHS")
    news_request = NewsRequest(
        months=MONTHS, news_category=NEWS_CATEGORY, search_phrase=SEARCH_PHRASE
    )

    setup(news_request)


if __name__ == "__main__":
    try:
        main()
    finally:
        close_browser()
