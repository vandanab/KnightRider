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
import cjson

PINS_FILE = "/media/08A7089D4E9B9DB1/study/TAMU/pinterest/KnightRider/src/pinterest/pins.json"
USER_FILE = "/media/08A7089D4E9B9DB1/study/TAMU/pinterest/KnightRider/src/pinterest/users.json"

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
        
    def write_to_file_json(self, file_name, data):
    	f = open(file_name, 'a')
    	f.write(cjson.encode(data))
    	f.close()
    	
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
        pin_data = {}
        fail_count = 0
        
        def get_count(class_id):
            count = pin.find(class_=class_id)
            if count:
                count_split = count.get_text().strip().split()
                if count_split: return int(count_split[0])
                else: return 0
            else: return 0
            
        # populate user data structure
        #get location
        while fail_count < 10:
				user_id = bs.find(class_= "selected").get('href')
				user_data['user_id'] = user_id
				location = bs.find('li', attrs={'id' : 'ProfileLocation'})
				if location != None:
					#print location.contents[2]
					#loc = str(location.contents[2])
					user_data['location'] = location.contents[2]      
				
				#collecting user data number of boards, pins, likes, followers, following
				#boards, pins, likes, followers, following
				bpl =  bs.find('ul', attrs={'class' : 'links'})
				if bpl != None:
					atags = bpl.findAll('a')
					for atag in atags:
						if(len(atag.contents) > 2):
							num = atag.contents[1].contents[0]
							ntypes = str(atag.contents[2])
							user_data[ntypes.strip()] = str(num)
		
				ff = bs.find('ul', attrs={'class' : 'follow'})
				if ff:
					atags = ff.findAll('a')
					for atag in atags:
						if(len(atag.contents) > 2):
							num = atag.contents[1].contents[0]
							ntypes = str(atag.contents[2])
							user_data[ntypes.strip()] = str(num)
				user_data['boards'] = []
			
				# Go to the board URL and get all the pins of that board
				boards = bs.find_all('div', attrs={'class':'board'})
				for board in boards:
					atag = board.find('a')
					board_url = self.base_url + atag['href']
					pin_data['user_id'] = user_id
					pin_data['board-id'] = atag['href']
					user_data['boards'].append(atag['href'])
					html = util.get_contents(board_url)
					if html != None:
						bs = BeautifulSoup(html)
						pins = bs.find_all('div', attrs={'class':'pin'})
						for pin in pins:
							pin_data['id'] = pin['data-id']
							pin_data['description'] = pin.find(class_='description').get_text()
							pin_data['Comments_count'] = get_count('CommentsCount')
							pin_data['Likes_count'] = get_count('LikesCount')
							pin_data['Repin_count'] = get_count('RepinsCount')
							links = pin.find_all(class_ = 'convo attribution clearfix')
							self.write_to_file_json(PINS_FILE, pin_data)     				
							for link in links:
								atag = link.find('a')
								if atag != None:
									pin_data['link'] = atag['href']
						
				self.write_to_file_json(USER_FILE, user_data)
				# user_data - dictionary DS with user data ,need to pass it to get_json
				# constructing 'following' link
				
				page = []
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
