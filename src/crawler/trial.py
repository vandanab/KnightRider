'''
Created on Sep 7, 2012

@author: vandana
'''

import httplib2
import sys

def main(argv=None):
    http = httplib2.Http()
    (header, pagehtml) = http.request("http://www.pinterest.com", 'GET')
    print pagehtml
    
if __name__ == "__main__":
    sys.exit(main())