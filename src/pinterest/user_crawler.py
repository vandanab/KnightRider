'''
Created on Sep 19, 2012

@author: vandana
Module for crawling pinterest.com user data.
'''

from crawler.base import Crawler
from bs4 import BeautifulSoup
import httplib2
import sys 

class UserCrawler(Crawler):
    def __init__(self):
        self.base_url = "http://www.pinterest.com"
        Crawler.__init__(self)
    
    def get_start_links(self):
        # sensitive to html structure
        links = []
        http = httplib2.Http()
        (header, pagehtml) = http.request(self.base_url, 'GET')
        # process header to make sure that the response is a valid response
        
        bs = BeautifulSoup(pagehtml)
        bs.prettify()
        pins = bs.find_all('div', attrs={'class':'pin'})
        for i in pins:
            div = i.find('div', attrs={'class': 'convo attribution clearfix'})
            p_tag = div.find('p')
            a_tags = p_tag.find_all('a');
            
            tuples = a_tags[0].attrs
            for t in tuples:
                if t == "href":
                    links.append(self.base_url + tuples[t])
            if len(a_tags) == 3:
                tuples = a_tags[1].attrs
                for t in tuples:
                    if t == "href":
                        links.append(self.base_url + tuples[t])
        return links;
    
    def process_html(self, html):
        """
        """
        # we don't want to save the entire content - not very useful.
        bs = BeautifulSoup(html)
        bs.prettify()
        links = []
        # process the page for complete user profile, all attributes etc
        # the board/pin urls
        # stats
        # followers and following network
        return links

def main(argv=None):
    uc = UserCrawler()
    uc.crawl();

if __name__ == "__main__":
    sys.exit(main())  
