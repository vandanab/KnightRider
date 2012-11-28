'''
Created on Sep 19, 2012

@author: vandana
Module for crawling pinterest.com user data.
'''

from src.crawler.base import Crawler
from bs4 import BeautifulSoup
from src.common import util
from src.common.settings import USERS_FILE, PINS_FILE
import sys 
import cjson
import logging

class UserCrawler(Crawler):
  
  def __init__(self):
    self.base_url = "http://www.pinterest.com"
    Crawler.__init__(self)

  
  def get_soup(self, url):
    page_content = util.get_contents(url, self.RETRY_COUNT)
    if page_content == None:
      logging.debug("no html content fetched after %s retries." %
                    str(self.RETRY_COUNT))
      return None
    soup = BeautifulSoup(page_content)
    soup.prettify()
    return soup

  
  def get_start_links(self):
    # sensitive to html structure
    links = []
    page_html = util.get_contents(self.base_url, self.RETRY_COUNT)
    if page_html != None:
      bs = BeautifulSoup(page_html)
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
    return links

        
  def write_to_file_json(self, file_name, data):
    f = open(file_name, 'a')
    f.write(cjson.encode(data)+'\n')
    f.close()
      

  def process_html(self, html):
    """
    Given a user page html, this function will get all the information of the user
    - Number of Boards, Pins, Likes, Followers, Following, Location (if specified)
    Also, it will construct the user's following page URL, get it's HTML and find 
    who all this user is following and will pass them to the crawler.
    """
    
    print "Trace : Processing html...\n"
    bs = BeautifulSoup(html)
    bs.prettify()
    
    user_data = self.get_user_data(bs)
    self.write_to_file_json(USERS_FILE, user_data)
               
    return self.get_follower_following_links(user_data['user'])
  
  
  def get_follower_following_links(self, user):
    links = []
    followers_soup = self.get_soup(self.base_url + '/%s/followers/' % user)
    if followers_soup != None:
      links.extend([self.base_url + p.get('href') for p in 
                    followers_soup.find_all(class_ = 'PersonImage ImgLink')])
    following_soup = self.get_soup(self.base_url + '/%s/following/' % user)
    if following_soup != None:
      links.extend([self.base_url + p.get('href') for p in 
                    following_soup.find_all(class_ = 'PersonImage ImgLink')])
    return links

  def load_meta_info_from_soup(self, soup):
    info = {}
    for meta in soup.find_all('meta'):
      if meta.get('property') and ('pinterestapp' in meta.get('property') or
                                   'og' in meta.get('property')):
        info[meta.get('property').split(':')[1]] = meta.get('content')
    return info

  
  def get_user_statistics(self, soup, user_data, class_id):
    bpl =  soup.find('ul', attrs={'class' : class_id})
    if bpl != None:
      atags = bpl.find_all('a')
      for atag in atags:
        if(len(atag.contents) > 2):
          num = atag.contents[1].contents[0]
          ntypes = str(atag.contents[2])
          num = str(num).replace(',', '') 
          user_data[ntypes.strip().lower()+'_count'] = int(num)

  
  def get_user_data(self, soup):
    user_data = {}
    username = soup.find(class_ = "selected").get('href').strip('/')
    user_data['user'] = username
    user_data['id'] = (soup.find('a', attrs={'href': '/user/block/'}))['user_id']
    location = soup.find('li', attrs={'id' : 'ProfileLocation'})
    if location != None:
      user_data['location'] = location.contents[2]
    #get number of boards, pins, likes, followers, following
    self.get_user_statistics(soup, user_data, 'links')
    self.get_user_statistics(soup, user_data, 'follow') 
    #get boards
    user_data['boards'] = self.get_boards_data(soup, user_data['user'])
    return user_data


  def get_boards_data(self, soup, user):
    boards_data = []
    boards = soup.find_all('div', attrs={'class':'pin pinBoard'})
    #boards = soup.find_all('div', attrs={'class':'board'})
    for board in boards:
      board_id = board['id'].strip('board')
      #board_id = ''
      #atag = board.find('a')
      #board_url = self.base_url + atag['href']
      board_url = self.base_url + '/board/%s/' % board_id
      pins, page_id = [], 0
      pin_count = 0
      board_data = {}
      while True:
        soup = self.get_soup(board_url+'?page=%s'%page_id)
        if page_id == 0:
          board_data = self.get_board_data(soup, board_id)
        pins_on_page = map(self.get_pin_data,
                           soup.find_all('div', attrs={'class':'pin'}))
        for pin in pins_on_page:
          if 'pin_user' not in pin: pin['pin_user'] = user
          pin['board_id'] = board_id
        if pins_on_page:
          pins+=pins_on_page
          pin_count += len(pins_on_page)
        else: break
        if pin_count >= board_data['pins_count']:
          break
        page_id+=1
      boards_data.append(board_data)
      for pin in pins:
        self.write_to_file_json(PINS_FILE, pin)
    return boards_data


  def get_board_data(self, soup, board_id):
    board_data = {}
    board_data['id'] = board_id
    board_meta_info = self.load_meta_info_from_soup(soup)
    board_data['title'] = board_meta_info['title']
    board_data['desc'] = board_meta_info['description']
    board_data['category'] = board_meta_info['category']
    board_data['url'] = board_meta_info['url'].split('/')[-1]
    board_data['followers_count'] = int(board_meta_info['followers'])
    board_data['pins_count'] = int(board_meta_info['pins'])
    return board_data

    
  def get_pin_data(self, pin):
    def get_count(class_id):
      count = pin.find(class_=class_id)
      if count:
        count_split = count.get_text().strip().split()
        if count_split: return int(count_split[0])
        else: return 0
    pin_id = pin.get('data-id')
    image_url = pin.find(class_='PinImageImg').get('src')
    pin_data = {
                'id': pin_id,
                'comment_count': get_count('CommentsCount'),
                'like_count': get_count('LikesCount'),
                'repin_count': get_count('RepinsCount'),
                'description': pin.find(class_='description').get_text(),
                'url': '/pin/%s'%pin_id,
                'image_url': image_url,
                'original_id': image_url.split('/')[-1].split('_')[0],
    }
    links = pin.find(class_='convo attribution clearfix').find_all('a')
    if links:
      pin_data['source_url'] = links[-1].get('href')
      if links[-1].get('href')!=links[0].get('href'): 
        pin_data['pin_user'] = links[0].get('href')[1:-1]
      else: pin_data['source_url'] = '' 
    return pin_data


def main(argv=None):
  uc = UserCrawler()
  uc.crawl();

if __name__ == "__main__":
  sys.exit(main())