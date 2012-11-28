"""
Created on Sep 19, 2012

@author: vandana
Basic web crawler
"""

from abc import abstractmethod
from src.common.data_structures import MongoQueue
import httplib2
import time
import logging

class Crawler:
  """
  A basic web crawler which starts off with a set of links.
  
  It declares abstract methods for processing domain specific html
  and extracting links and seed the crawler which need to be implemented by
  application or domain specific derived crawlers.
  """
  RETRY_COUNT = 2
  
  def __init__(self, start_links=None):
    # look up optimized queue
    if start_links:
      self.unvisited_urls = MongoQueue("unvisited", start_links)
    else:
      self.unvisited_urls = MongoQueue("unvisited")
    more_links = self.get_start_links()
    self.unvisited_urls.extend(more_links)
    print self.unvisited_urls
    
    # set of visited urls
    self.visited_urls = MongoQueue("visited")
    
    # make sure to arrange for caching if the above lists end up
    # being a database
    #self.current_link = None;
    logging.basicConfig(filename='crawler.log',level=logging.DEBUG)

    #can be a static method
  def crawl(self):
    """
    crawls pages in breadth-first fashion by inserting links into the
    queue
    at a given point starts from a single link and traverses as far as it
    can and makes sure it does the required memory management
    """
    
    http = httplib2.Http()
    while self.unvisited_urls:
      link = self.unvisited_urls.dequeue()
      retry_count = self.RETRY_COUNT
      while retry_count > 0:
        (header, pagehtml) = http.request(link, 'GET')
        try:
          if header['status'] == '200':
            urls = self.process_html(pagehtml)
            self.visited_urls.enqueue(link)
            for i in urls:
              if i in self.visited_urls or i in self.unvisited_urls:
                continue
              self.unvisited_urls.enqueue(i)
            break
          else:
            logging.debug('Request Failed: %s status' % header['status'])
            logging.debug("Response Header: %s", header)
            retry_count -= 1;
            time.sleep(120) #sleep for 2 mins before continuing
            logging.info("Retrying...")
        except:
          logging.debug('Some error occurred.')
          break      
    
    #might not be needed
  def continue_crawl(self):
    # start from the current_link
    pass
  
  def handle_error(self):
    # any kind of spurious situations which occur need to be handled
    pass
  
  def get_start_links(self):
    """
    Derived classes may implement to add more start links
    """
    return []
  
  @abstractmethod
  def process_html(self):
    """
    Extracts urls and processes the html according to requirements
    """
    raise NotImplementedError
         

class ReturnValues:
  CRAWL_STOPPED_EMPTY = 3 #crawl stopped as queue became empty


class CrawlType:
  PINS = 1
  USERS = 2