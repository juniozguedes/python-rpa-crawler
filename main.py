import os
import sys
import ast
from crawler import NyScrapper
import configparser
from schemas import NewsRequest
from RPA.Robocorp.WorkItems import WorkItems


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
    # config = initialize_config()
    work_item = WorkItems()
    work_item.get_input_work_item()
    SEARCH_PHRASE = work_item.get_work_item_variable("search_phrase")
    NEWS_CATEGORY = work_item.get_work_item_variable("category")
    MONTHS = work_item.get_work_item_variable("months")
    check_dependencies()
    # Accessing values from the configuration
    # SEARCH_PHRASE = config.get("General", "SEARCH_PHRASE")
    # NEWS_CATEGORY = config.get("General", "NEWS_CATEGORY")
    # NEWS_CATEGORY = ast.literal_eval(NEWS_CATEGORY)
    # MONTHS = config.getint("General", "MONTHS")
    news_request = NewsRequest(
        months=MONTHS, news_category=NEWS_CATEGORY, search_phrase=SEARCH_PHRASE
    )

    # Declaring object and running orchestrator
    obj = NyScrapper()
    try:
        if obj.setup(news_request):
            # Exits with status 0 if success
            sys.exit(0)
        sys.exit(1)
    finally:
        obj.close_browser()


if __name__ == "__main__":
    main()
