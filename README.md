# Common Crawler

Super simple Python 3 functions that can scrape the Common Crawl dataset (https://github.com/jpbm/common_crawler)

Heavily inspired by the works of others, especially:
https://www.bellingcat.com/resources/2015/08/13/using-python-to-mine-common-crawl/
https://www.cedar.net.au/using-python-and-common-crawl-to-find-products-from-amazon-com/

There's a generator in 'src/get_records.py' that can be used to download common crawl records and some utility function in 'src/get_html.py' that can be used to get just the html from the records.

# Input:
Search domain (ex. https://www.nytimes.com/section/politics).

# Output:
List of strings containing common crawl metadata + the scraped HTML file.

# Usage:
See: common_crawler.ipynb
