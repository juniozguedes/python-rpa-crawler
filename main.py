import os
import sys
import ast
from crawler import close_browser, setup
import configparser
from schemas import NewsRequest


def initialize_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def check_dependencies():
    """Checks if the src folder exists
    This folder will be responsible for the Vault part"""
    root_directory = os.getcwd()
    folder_name = "src"
    folder_path = os.path.join(root_directory, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")


def main():
    """Start main function for RPA for news search^
    Initialize env variables and global configs"""
    config = initialize_config()
    check_dependencies()
    # Accessing values from the configuration
    SEARCH_PHRASE = config.get("General", "SEARCH_PHRASE")
    NEWS_CATEGORY = config.get("General", "NEWS_CATEGORY")
    NEWS_CATEGORY = ast.literal_eval(NEWS_CATEGORY)
    MONTHS = config.getint("General", "MONTHS")
    news_request = NewsRequest(
        months=MONTHS, news_category=NEWS_CATEGORY, search_phrase=SEARCH_PHRASE
    )

    if setup(news_request):
        # Exits with status 0 if success
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    finally:
        close_browser()
