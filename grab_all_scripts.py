import urllib2
from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup( urllib2.urlopen("http://www.imsdb.com/all%20scripts/" ) )

movie_ident = '/Movie Scripts/'

links_list = [link.get('href') for link in soup.findAll('a') if link.get('href').find(movie_ident) != -1][5:]

begin_url = "http://www.imsdb.com"
completed_links = [ begin_url + i.replace(' ', '%20') for i in links_list ]

with open('script_links.txt', 'w') as file:
	for link in completed_links:
		file.write(link + '\n')