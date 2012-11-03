'''
Created on Oct 31, 2012

@author: vandana
'''
import httplib2

def get_contents(url):
	http = httplib2.Http()
	(header, pagehtml) = http.request(url, 'GET')
	#print header
	if header['status'] == '200':
		return pagehtml
	else:
		return None

if __name__ == '__main__':
	r = get_contents('http://google.com')
	print r
