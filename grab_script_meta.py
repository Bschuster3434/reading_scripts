import urllib2
from BeautifulSoup import BeautifulSoup

def grab_script_meta(meta_url):
	soup = BeautifulSoup( urllib2.urlopen( meta_url ) )