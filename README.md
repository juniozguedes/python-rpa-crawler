# Dependencies

Dependencies are listed in requirements.txt

- pandas to generate excel
- configparser to store general environment
- pydantic for data validation and typing

# Install

```
pip install -r requirements.txt
```

# Run the crawler

To start the application we want to execute the main.py file

```
python .\main.py
```

# Considerations

- This project consists of a RPA (Robot Process Automation) script that will open the nytimes.com website.
- Collect data from config.ini (Search Phrase, Categories and Months (1,2,3))
- Search the search phrase along with categories (if provided) and months
- After iterating through all posts, the application will create a folder for this search inside src/
- The application will save all imgs in src/{search_phrase}/img
- The application will generate an excel file with significant data in src/{search_phrase}/news.xlsx
- If all runs well the log will indicate success and exit graciously

# Performance considerations

- Some searchs can lead to hundreds of thousands results.
- There is a function called load_more() being called in crawler.py at iterate_news() function
- This function always search for the "Load more" button at the bottom of the news page
- This can increase the amount of time that the script will take to finish
- To check only the first 10 news posts, comment the line that the load_more() is being called.
