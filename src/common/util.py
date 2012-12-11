'''
Created on Oct 31, 2012

@author: vandana
'''
import httplib2

def get_contents(url, retry_count=0):
	http = httplib2.Http()
	(header, pagehtml) = http.request(url, 'GET')
	fail_count = 0;
	while True and fail_count < retry_count:
		if header['status'] == '200':
			return (header, pagehtml)
		else:
			fail_count += 1
			print header
			print 'Exception while crawling. Retrying...'
	return (header, None)

if __name__ == '__main__':
	r = get_contents('http://google.com')
	print r
