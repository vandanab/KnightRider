'''
Created on Sep 19, 2012

@author: vandana
Module for crawling pinterest.com data.
We are looking to collect the pins and users data.
'''

from BeautifulSoup import BeautifulSoup
from base import Crawler
import httplib2
import re
import sys

class PinsCrawler(Crawler):
    def __init__(self):
        self.base_url = "http://www.pinterest.com"
        self.start_links = ["http://www.pinterest.com",
                            "http://www.pinterest.com/all/"]
        self.start_links.extend(self.get_start_links())
        #print self.start_links
        Crawler.__init__(self, self.start_links)
    
    def get_start_links(self):
        links = []
        http = httplib2.Http()
        (header, pagehtml) = http.request(self.base_url, 'GET')
        # process header to make sure that the response is a valid response
        
        bs = BeautifulSoup(pagehtml);
        bs.prettify()
        
        # get lazy load page links upto 10 pages
        links.extend(self.get_lazy_load_links(self.base_url, 10))
        
        # looking for category specific links
        a_tags = bs.findAll(href=re.compile("\?category="))
        for i in a_tags:
            tuples = i.attrs
            for t in tuples:
                if t[0] == "href":
                    links.append(self.base_url + t[1]);
        
        # looking for gifts links
        a_tags = bs.findAll(href=re.compile("/gifts/\?"))
        for i in a_tags:
            tuples = i.attrs
            for t in tuples:
                if t[0] == "href":
                    links.append(self.base_url + t[1]);
        return links
    
    def get_lazy_load_links(self, url, num_pages):
        separator = ""
        if re.match("\?", url):
            separator = "&"
        else:
            separator = "/?"
        links = []
        for i in range(num_pages):
            links.append(url + separator + "lazy=1&page=" + str(i+1))        
        return links
    
    def process_html(self, html):
        """
        """
        # we don't want to save the entire content - not very useful.
        bs = BeautifulSoup(html)
        bs.prettify()
        pins = bs.findAll('div', attrs={'class':'pin'})

        # process pins into pin objects
        # take care of gift pins as they have a price attached to it
        #print pins
        f = open('pinterest.html', 'w')
        f.write(html)
        #print html
        # extract pin category urls to crawl
        links = []
        for i in pins:
            div = i.find('div', attrs={'class': 'convo attribution clearfix'})
            p_tag = div.find('p')
            a_tags = p_tag.findAll('a');
            # the last url is the board url its pinned under by the user
            tuples = a_tags[len(a_tags) - 1].attrs
            for t in tuples:
                if t[0] == "href":
                    link = self.base_url + t[1];
                    links.append(link)
        return links
        

class UserCrawler(Crawler):
    def __init__(self):
        self.base_url = "http://www.pinterest.com"
        self.start_links = self.get_start_links()
        Crawler.__init__(self, self.start_links)
    
    def get_start_links(self):
        # very sensitive to html structure
        links = []
        http = httplib2.Http()
        (header, pagehtml) = http.request(self.base_url, 'GET')
        # process header to make sure that the response is a valid response
        
        bs = BeautifulSoup(pagehtml)
        bs.prettify()
        pins = bs.findAll('div', attrs={'class':'pin'})
        for i in pins:
            div = i.find('div', attrs={'class': 'convo attribution clearfix'})
            p_tag = div.find('p')
            a_tags = p_tag.findAll('a');
            #print a_tags

            tuples = a_tags[0].attrs
            if len(a_tags) == 3:
                tuples.extend(a_tags[1].attrs)
            for t in tuples:
                if t[0] == "href":
                    link = self.base_url + t[1];
                    links.append(link)
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
    #pc = PinsCrawler();
    #pc.crawl();
    uc = UserCrawler()
    uc.crawl();

if __name__ == "__main__":
    sys.exit(main())  
