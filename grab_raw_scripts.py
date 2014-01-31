import urllib2
from BeautifulSoup import BeautifulSoup
import pandas as pd
import csv
import itertools
from random import sample, randint, choice
import time
import re

def return_clean_script(script_url):
	
	dirty_text = grab_dirty_script(script_url)
	clean_text = text_cleaner(dirty_text)
	result = is_text_clean(clean_text)
	
	if result == True and len(clean_text) > 1000:
		return clean_text
	else:
		return None
	

def grab_dirty_script(script_url):
	"""
	Grabbing the raw script, one url at a time.
	"""
	try:
		soup = BeautifulSoup( urllib2.urlopen( script_url ) )
	except UnicodeEncodeError:
		print "Unicode Error with " + str(script_url)
		return "           "
	
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
	
def is_text_clean(text_body):

	text_body = str(text_body)
	
	string_tester = re.compile('<.*>')
	result = string_tester.match(text_body)
	
	if result == None:
		return True
	else:
		return False

def text_cleaner(text):
	text = str(text)
	loc = text.find('<br />')
	text = text[:loc]
	text = text.replace("</b>", "")
	text = text.replace("<b>", "")
	text = text.replace("</pre", "")
	text = text.replace("</pre>", "")
	text = text.replace("<body>", "")
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
	
def grab_specific_script_soup(file):
	soup = BeautifulSoup( urllib2.urlopen( file ) )
	return soup
	
def text_re():
	str1 = "<meta charset=\"utf-8\" />"
	str2 = "This is my testing string"
	str3 = "<b> I am going to the store </b>"
	
	p = re.compile('<.*>')
	
	assert p.match(str1) != None
	assert p.match(str2) == None
	assert p.match(str3) != None
	
	return "Successful Test"
	

def test_add_scripts():
	script_file = "test_script.csv"
	directory = "test_raw_script"
	
	s_df = pd.read_csv(script_file)
	s_df['Raw_Script_Loc'] = s_df['Raw_Script_Loc'].astype(object)
	r_row = choice(s_df[ pd.isnull( s_df['Raw_Script_Loc'] ) ].index)
	
	script_url = s_df['Raw_Script_URL'].ix[r_row]
	script_name = s_df['Script_Title'].ix[r_row]
	
	c_script = return_clean_script(script_url)
	
	if c_script != None:
		write_file = directory + '/' + script_name + '.txt'
		with open(write_file, 'w') as w_file:
			w_file.write(c_script)
		s_df['Raw_Script_Loc'].ix[r_row] = write_file
		s_df.to_csv(script_file, index = False)
	else:
		s_df['Raw_Script_Loc'].ix[r_row] = "unclean"
		print "Did not pass clean test"
		
def add_scripts():
	script_file = "script.csv"
	directory = 'raw_Script'
	
	s_df = pd.read_csv(script_file)
	s_df['Raw_Script_Loc'] = s_df['Raw_Script_Loc'].astype(object)
	
	length = len( s_df[ pd.isnull( s_df['Raw_Script_Loc'] ) ].index )
	
	for i in range(length):
	
		r_row = choice(s_df[ pd.isnull( s_df['Raw_Script_Loc'] ) ].index)
	
		script_url = s_df['Raw_Script_URL'].ix[r_row]
		script_name = s_df['Script_Title'].ix[r_row]
	
		c_script = return_clean_script(script_url)
	
		if c_script != None:
			write_file = directory + '/' + script_name + '.txt'
			with open(write_file, 'w') as w_file:
				w_file.write(c_script)
			s_df['Raw_Script_Loc'].ix[r_row] = write_file
			s_df.to_csv(script_file, index = False)
		else:
			s_df['Raw_Script_Loc'].ix[r_row] = "unclean"
			print "Did not pass clean test"
			
		time.sleep(2)
	
