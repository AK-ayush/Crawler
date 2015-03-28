#import urllib2
from proxy import urllib2
import urlparse
import socket
import os,sys
from bs4 import BeautifulSoup

#default timeout is 10 sec
socket.setdefaulttimeout(10)

# seed to spider
url = "http://trai.gov.in/Content/PressReleases.aspx"


def first_spider(seed):
	urls = [seed] #queue of urls to scrape,#frontier 
	visited = [] # historic record of urls
	dwnld = []
	while len(urls)>0:
		url = urls[0]
		urls.pop(0)
		if url in visited:
			break
		else:
			visited.append(url)
			try:
				htmlText = urllib2.urlopen(url).read()
				soup = BeautifulSoup(htmlText)
			except:
				pass
			for tag in soup.find_all('a'):
				href = tag.get('href')
				if href and not 'javascript' in href: 
					if href and '#' in href:		#To remove the anchor or reference
						ind = href.rfind('#')
						href = href[:ind-1]
					if href and not 'http' in href:
						en_href = urllib2.quote(href.encode('utf8'))#url encoding
						en_href = urlparse.urljoin(url,en_href)
					#Canonicalization of the urls extracted form the page
					en_href = en_href.lower()
					en_href = en_href.strip()
					path,ext = os.path.splitext(en_href)
					if ext == '.pdf' and not en_href in dwnld:
						dwnld.append(en_href)
						break
					if not en_href in urls:
						urls.append(en_href)
	return dwnld

dwnld = first_spider(url);
os.mkdir('files')
pwd = os.getcwd()
path = os.path.join(pwd,'files')
os.chdir(path)
for link in dwnld:
	print link
	os.system(' wget --tries=2 '+link)


