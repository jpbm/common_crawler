"""
Utility functions that search for, and download Common Crawl records.

CC records are stored on Amazon servers in WARC format, which contains gzip compressed html files along with some useful metadata about the size of the entry and the date on which it was scraped.

To retrieve Common Crawl data corresponding to a particular date, one must specifiy the 'index', which has the format of '2018-13', '2018-09' and thelike. The full list of indexes can be found here: http://index.commoncrawl.org/. A default index list is hardcoded into the 'get_records_gen' function.
"""

from urllib.parse import quote
import requests
import json

def get_entries_gen(domain,index_list=None):
    """
    Generator that returns Common Crawl entries for a search domain as a list of dictionaries. The entries contain the metadata necessary to know where the bytes of records are located. Each entry is a dictionay/json.
    
    The dictionaries have keys:
    'digest', 'filename', 'length', 'mime', 'mime-detected', 'offset', 'status', 'timestamp', 'url', 'urlkey'
    
    Fields have [str] format.
    
    Takes: 
    domain [str] (ex. https://www.nytimes.com/section/politics)
    index_list [iter] (optional) (ex. ['2018-13'])
    
    Returns:
    records [list] 
    """
    
    # default index list: full list
    if not index_list:
        index_list = download_index_list() 

    # yield records
    records = []
    for index in index_list:
        cc_url = "http://index.commoncrawl.org/CC-MAIN-%s-index?url=%s&output=json" % (index,quote(domain))
        response = requests.get(cc_url)
        
        if response.status_code == 200:
            for record in response.content.splitlines():
                yield json.loads(record)
        else: 
            print("get_entries: Code %s / %s" % (response.status_code,cc_url))



from io import BytesIO
import gzip


def download_record(record):
    """
    Takes:
    record [dict]
    
    Returns:
    record [str] (contains cc metadata and html document)
    """
    
    # start and end bytes within WARC file.
    start = int(record['offset'])
    end = start + int(record['length']) -1
    
    # retrieve data (html compressed as gzip)
    s3_url = 'https://commoncrawl.s3.amazonaws.com/'
    response = requests.get(
        s3_url+record['filename'],
        headers = {'Range': 'bytes=%i-%i' % (start,end)}
                           )
    
    assert response.status_code == 206
    
    
    return gzip.GzipFile(
        fileobj=BytesIO(response.content)
    ).read().decode('utf-8')


def get_records_gen(domain,index_list=None):
    """
    Generator that returns the Common Crawl records for a particular search domain.

    Takes:
    domain [str]

    Returns:
    record [str]
    """

    entries = get_entries_gen(domain,index_list)
    for entry in entries:
        yield download_record(entry)


import json

def download_index_list():
    """
    Download the full Common Crawl Index list
    
    Returns:
    index_list [list] (ex. ['2018-13','2018-09',...]
    """
    """ Common Crawl Indices """

    index_list_url = 'http://index.commoncrawl.org/collinfo.json'
    
    return [index['id'].replace('CC-MAIN-','') for index in json.loads(requests.get(index_list_url).content.decode('utf-8'))]

