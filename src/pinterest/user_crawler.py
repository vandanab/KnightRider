'''
Created on Sep 19, 2012

@author: vandana
Module for crawling pinterest.com user data.
'''

from src.crawler.base import Crawler
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
        Given a user page html, this function will get all the information of the user
        - Number of Boards, Pins, Likes, Followers, Following, Location (if specified)
        Also, it will construct the user's following page URL, get it's HTML and find 
        who all this user is following and will pass them to the crawler.
        """
        # we don't want to save the entire content - not very useful.
        print "Trace : Processing html...\n"
        bs = BeautifulSoup(html)
        bs.prettify()
        links = []        
        user_data = {}
        
        # populate user data structure
        #get location
        location = bs.find('li', attrs={'id' : 'ProfileLocation'})
        if location != None:
        	loc = str(location.contents[2])
        	user_data['location'] = loc.strip()      
        
        #collecting user data number of boards, pins, likes, followers, following
		#boards, pins, likes, followers, following
		
        bpl =  bs.find('ul', attrs={'class' : 'links'})
        atags = bpl.findAll('a')
		#print atags
        
        for atag in atags:
			if(len(atag.contents) > 2):
				num = atag.contents[1].contents[0]
				ntypes = str(atag.contents[2])
				user_data[ntypes.strip()] = str(num)
		
    	ff = bs.find('ul', attrs={'class' : 'follow'})
    	atags = ff.findAll('a')
    	for atag in atags:
			if(len(atag.contents) > 2):
				num = atag.contents[1].contents[0]
				ntypes = str(atag.contents[2])
				user_data[ntypes.strip()] = str(num)
        print user_data
        
        # user_data - dictionary DS with user data ,need to pass it to get_json
        # constructing 'following' link
        
        a_tag = bs.find_all('a', attrs={'class' : 'selected'});
        for a in a_tag:        	
        	page = (self.base_url + a['href'] + "following")
        
        html1 = util.get_contents(page)
        if (html1 != None):
        	bs_follow = BeautifulSoup(html1)
        	divs = bs_follow.find_all('div', attrs={'class' : 'person'})
        	for div in divs:
        		atag = div.find('a')
        		links.append(self.base_url + atag['href'])
        		
        return links

def main(argv=None):
    uc = UserCrawler()
    uc.crawl();

if __name__ == "__main__":
    sys.exit(main())  
