'''
Created on Sep 19, 2012

@author: vandana
Module for crawling pinterest.com user data.
'''

from crawler.base import Crawler
from bs4 import BeautifulSoup
from src.common import util
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
        # page1 = html
        # page2 = get userid from html generate URL for userid/following
        # crawl page2 to get userids of persons the user is following div class="person", href = "/vistabill"
        # add new URLs to links
        # populate user data structure
        
        location = bs.find_all('span', attrs={'class' : 'icon location'})  
        #dynamic web pages?
        #location.content has the profile location
        
        li_tag = bs.find_all('li');
        a_tag = li_tag.find_all('a', attrs={'class' : 'selected'});
        tuples = a_tag[0].attrs
        for t in tuples:
        	if t == "href":
            	page1.append(self.base_url + tuples[t] + "following")
        	
        return links

def main(argv=None):
    uc = UserCrawler()
    uc.crawl();

if __name__ == "__main__":
    sys.exit(main())  
