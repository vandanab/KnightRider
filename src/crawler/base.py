"""
Created on Sep 19, 2012

@author: vandana
Basic domain specific crawler
"""
from BeautifulSoup import BeautifulSoup
from abc import abstractmethod 
from collections import deque
import httplib2

class Crawler:
    """
    
    """
    def __init__(self, start_links):
        # try to keep this stuff in database.
        # or load from database as this list might get bigger
        self.unvisited_urls = deque();
        self.unvisited_urls.extend(start_links)
        # this can be a database table too.
        self.visited_urls = [];
        
        # make sure to arrange for caching if the above lists end up
        # being a database
        self.current_link = None;        
    
    #can be a static method
    def crawl(self):
        """
        """
        # crawls pages in breadth-first fashion by inserting links into the
        # queue
        # at a given point starts from a single link and traverses as far as it
        # can and makes sure it does the required memory management
        http = httplib2.Http()
        while self.unvisited_urls:
            link = self.unvisited_urls.popleft()
            (header, pagehtml) = http.request(link, 'GET')
            # process header if needed especially for error response to slow
            # down or sleep
            # handle_error()
            urls = self.process_html(pagehtml);
            for i in urls:
                if i in self.visited_urls or i in self.unvisited_urls:
                    continue
                self.unvisited_urls(i)
        if not self.unvisited_urls:
            return ReturnValues.CRAWL_STOPPED_EMPTY
    
    #might not be needed
    def continue_crawl(self):
        # start from the current_link
        pass
    
    def handle_error(self):
        # any kind of spurious situations which occur need to be handled
        pass
    
    @abstractmethod
    def get_start_links(self):
        pass
    
    @abstractmethod
    def process_html(self):
        #extracts urls and processes the html according to requirements
        pass
         

class ReturnValues:
    CRAWL_STOPPED_EMPTY = 3 #crawl stopped as queue became empty


class CrawlType:
    PINS = 1
    USERS = 2