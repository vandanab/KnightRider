'''
Created on Oct 2, 2012

@author: vandana
'''

from crawler.base import Crawler
from bs4 import BeautifulSoup
import httplib2
import re
import sys

class PinsCrawler(Crawler):
    def __init__(self):
        self.base_url = "http://www.pinterest.com"
        links = ["http://www.pinterest.com",
                            "http://www.pinterest.com/all/"]
        Crawler.__init__(self, links)
    
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
        a_tags = bs.find_all(href=re.compile("\?category="))
        # looking for gifts links
        a_tags.extend(bs.find_all(href=re.compile("/gifts/\?")))
        
        for i in a_tags:
            tuples = i.attrs
            for t in tuples:
                if t == "href":
                    links.append(self.base_url + tuples[t]);
        
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
        pins = bs.find_all('div', attrs={'class':'pin'})

        # process pins into pin objects
        # take care of gift pins as they have a price attached to it
        #print pins
        
        # write html to a file if needed        
        #f = open('pinterest.html', 'w')
        #f.write(html)
        #print html
        
        # extract pin category urls to crawl
        links = []
        for i in pins:
            div = i.find('div', attrs={'class': 'convo attribution clearfix'})
            p_tag = div.find('p')
            a_tags = p_tag.find_all('a');
            # the last url is the board url its pinned under by the user
            tuples = a_tags[len(a_tags) - 1].attrs
            for t in tuples:
                if t[0] == "href":
          # is this correct? you are appending both users and boards to the same links. So will it be ok when we give these links to the crawler again?
                    link = self.base_url + t[1];	
                    links.append(link)
        return links

def main(argv=None):
    pc = PinsCrawler()
    #pc.crawl();

if __name__ == "__main__":
    sys.exit(main())
