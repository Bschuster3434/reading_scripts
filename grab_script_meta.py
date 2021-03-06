import urllib2
from BeautifulSoup import BeautifulSoup
import pandas as pd
import csv
import itertools
from random import sample, randint
import time


def grab_script_meta(meta_url):
	"""
	Returns all the meta_data, including the script url, into a dictionary
	"""
	soup = BeautifulSoup( urllib2.urlopen( meta_url ) )
	script_details_table = get_script_details_table(soup)
	
	dirty_title = soup.title.contents[0]
	clean_title = dirty_title[:dirty_title.find(' Script')]
	
	writer_genre_scripts = script_details_table.findAll('a')
	
	writers = [ i.contents[0] for i in writer_genre_scripts if i['href'].find('writer') != -1 and i.contents != []]
	genres = [ i.contents[0] for i in writer_genre_scripts if i['href'].find('genre') != -1 and i.contents != []]
	
	script_url = "http://www.imsdb.com/" + [ i.get('href') for i in writer_genre_scripts if i['href'].find('scripts') != -1][0]
	
	sdt_string = str(script_details_table)
	
	script_date = grab_string_details("Script Date", sdt_string)
	movie_release_date = grab_string_details("Movie Release Date", sdt_string)
	
	return {'title': clean_title, 'writers' : writers, 'genres' : genres, 'script_url' : script_url, 'script_date' : script_date, 'movie_release_date' : movie_release_date}
	
	

def grab_string_details(begin_search, string):
	"""
	Using the defined middle and end string for 'script date' and 'movie release', finds the exact string
	"""
	begin_string_search = string.find(begin_search)
	if begin_string_search == -1:
		return None
	mid = "</b> : "
	end = "<br />"
	
	start = begin_string_search + len(begin_search) + len(mid)
	end = string[start:].find(end) 
	
	info = string[start: start + end]
	
	return info
	
	
def get_script_details_table(soup):
	"""
	Grabs the specific table that has most of the pertainaint information
	"""
	all_tables = soup.findAll('table')

	for i in all_tables:
		try:
			result = i['class'] == 'script-details'
		except KeyError:
			continue
		if result == True:
			return i
			
def open_meta_links():
	"""
	Returns meta_links_id csv into a pandas object with title
	"""
	return pd.read_csv('meta_links_id.csv', names = ['id', 'page_link', 'downloaded_bool'])		
			

def mark_completed(id):
	"""
	Takes a csv file and list of Id's and alters the csv to mark the movie as 'collected'
	"""
	
	file = 'meta_links_id.csv'
	
	new_rows = []
	
	with open(file, 'rb') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			if int(row[0]) == int(id):
				row[2] = 1
			new_rows.append(row)
	
	with open(file, 'wb') as csv_file2:
		writer = csv.writer(csv_file2)
		writer.writerows(new_rows)	
		
def write_data_to_csvs(script_id, dict):
	"""
	Writes all the relevant values for the correct scripts and tells meta_links_id.csv that the script has been downloaded
	"""
	if dict['genres'] == None: raise Exception( str(script_id) + ' has not genre.' )
	elif dict['writers'] == None: raise Exception( str(script_id) + ' has no writers.' )
		
	
	script_list = [[script_id, dict['title'], dict['movie_release_date'], dict['script_date'], dict['script_url']]]
	genres_list = list(itertools.product(*[[script_id], dict['genres']]))
	writers_list = list(itertools.product(*[[script_id], dict['writers']]))
	
	with open('script.csv', 'ab') as script_file:
		writer = csv.writer(script_file)
		for row in script_list:
			writer.writerow(row)
		
	with open('genres.csv', 'ab') as script_file:
		writer = csv.writer(script_file)
		for row in genres_list:
			writer.writerow(row)
	
	with open('writers.csv', 'ab') as script_file:
		writer = csv.writer(script_file)
		for row in writers_list:
			writer.writerow(row)
	
	mark_completed(script_id)
	
	print str(script_id) + " has been written into files."
		
def grab_n_script_metas(n = 2):
	"""
	Grabs a random number of scripts defined by 'n'. Defaults to 1.
	"""
	
	meta_links = open_meta_links()
	grab_links = meta_links[meta_links['downloaded_bool'] == 0]
	n_links = sample(grab_links.index, n)
	
	curr_links = grab_links.ix[n_links]
	
	for index, row in curr_links.iterrows():
		script_id = row['id']
		script_url = row['page_link']
		
		print "Now on " + str(script_id)
		
		meta_dict = grab_script_meta(script_url)
		
		write_data_to_csvs(script_id, meta_dict)
		
		wait_seconds = randint(2, 6)
		time.sleep(wait_seconds)
		
	# {'title': clean_title, 'writers' : writers, 'genres' : genres, 'script_url' : script_url, 'script_date' : script_date, 'movie_release_date' : movie_release_date}
	
	
def test_wdtcsv():
	# {'title': clean_title, 'writers' : writers, 'genres' : genres, 'script_url' : script_url, 'script_date' : script_date, 'movie_release_date' : movie_release_date}
	
	details_list = {'script_id' : script_id, 'meta_link' : meta_link, 'binary' : binary}
	
	meta_dict = grab_script_meta(details_list['meta_link'])

	write_data_to_csvs(script_id, meta_dict)

	return "Test Completed"
	
	
	
	
	
	
	
	


