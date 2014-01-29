import urllib2
from BeautifulSoup import BeautifulSoup
import pandas as pd
import csv
import itertools
from random import sample, randint, choice
import time

def grab_script(script_url):
	"""
	Grabbing the raw script, one url at a time.
	"""
	soup = BeautifulSoup( urllib2.urlopen( script_url ) )
	
	#the Body tag might be appropriate, as well as pre
	#Might be two ways to pull out the script, one using the tag pre, the other body
	# soup.findAll('body')[-1] seems to work for most, but there are a few notable exceptions
	# in which case, soup.findAll('pre')[-1] works.
	# In either case, '<br />' seems to be the final break point, which is good.

	print script_url
	if soup.findAll('pre')[-1].contents == [] or soup.findAll('pre')[-1].contents == ['\n']:
		text_body = soup.findAll('body')[-1]
	else:
		text_body = soup.findAll('pre')[-1]
	
	return text_body

def text_cleaner(text):
	text = str(text)
	loc = text.find('<br />')
	text = text[:loc]
	text = text.replace("</b>", "")
	text = text.replace("<b>", "")
	text = text.replace("</pre", "")
	text = text.replace("</pre>", "")
	return text
	
	
def grab_random_script():
	df = pd.read_csv('script.csv')
	file = choice(df['Raw_Script_URL'])
	text_body = grab_script(file)
	return text_body
	
def grab_random_soup():
	df = pd.read_csv('script.csv')
	file = choice(df['Raw_Script_URL'])
	soup = BeautifulSoup( urllib2.urlopen( file ) )
	return soup