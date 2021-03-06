import pandas as pd
import json
import urllib2
import time
import sys

r_file = 'rotten_ids.csv'

r_df = pd.read_csv('rotten_ids.csv')

def open_null_rt_files():
	file = 'rotten_ids.csv'
	df = pd.read_csv(file)
	df['rt_title'] = df['rt_title'].astype(str)
	t_df = df[~pd.isnull(df.rt_id) ]
	b_df = df[ pd.isnull(df.rt_id) ]
	return t_df, b_df


def append_info_to_csv(dataframe, head = True, by = 'title'):
	"""
	Appends the first five values (or the entire sheet) worth of new info from rotten tomatoes
	to the dataframe passed to the function.
	"""
	
	if head == True:
		df = dataframe.head()
	else:
		df = dataframe

	for i in df.index:
		s_title = df['Script_Title'].ix[i]
		rt_id = df['rt_id'].ix[i]
		print "Now Printing " + s_title
		#Below if statement decides if we're searching by id or title
		if by == 'title':
			rt_dict = grab_rt_info(s_title)
		elif by == 'id':
			rt_dict = grab_rt_info(rt_id, by = by)
		else:
			raise Exception('by needs to be either "title" or "id"')	
			
		if rt_dict == None:
			continue
		try:	
			df['rt_id'].ix[i] = rt_dict['id']
			df['rt_year'].ix[i] = rt_dict['year']
			df['rt_title'].ix[i] = rt_dict['title']
			df['rt_critics_score'].ix[i] = rt_dict['critics_score']
			df['rt_audience_score'].ix[i] = rt_dict['audience_score']
		except ValueError:
			continue

		time.sleep(.25)
		
	

def grab_rt_info(value , by = 'title'):
	"""
	This function pulls in all the relevant rotten tomatoes information for each movie.
	Uses the 'Movies Search' api query to movies
	Search Rotten Tomatoes API Documentation for more information
	"""
	
	api_key = 'beg2csvf5vv2d45tfdqfgegr'
	
	if by == 'title':
		url_begin = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?q="
		url_end = "&page_limit=1&page=1&apikey="
	
		c_title = title_transform(value)
	
		url = url_begin + c_title + url_end + api_key
	
	if by == 'id':
		url_begin = "http://api.rottentomatoes.com/api/public/v1.0/movies/"
		url_end = ".json?apikey="
		
		url = url_begin + str(value) + url_end + api_key
	
	else:
		raise Exception('by needs to equal "title" or "id"')
		sys.exit(0)
	
	page = json.loads(urllib2.urlopen(url).read())
	movie_info = {}
	
	try:
		if page['total'] == 0:
			return None
	except KeyError:	
		pass
		
	try:
		movie = page['movies'][0]
	except KeyError:
		movie = page
		
	movie_info['id'] = movie['id']
	movie_info['year'] = movie['year']
	movie_info['title'] = movie['title']
	
	
	ratings = movie['ratings']
	movie_info['critics_score'] = ratings['critics_score']
	movie_info['audience_score'] = ratings['audience_score']
	
	return movie_info
	
def title_transform(str):
	"""
	Removes the special characters from the title of the movie and replaces them with appropriate characters.
	For use with RT API string search
	"""
	str = str.replace(",", "%2C")
	str = str.replace(" ", "+")
	str = str.replace("/", "%2F")
	str = str.replace(":", "%3A")
	return str	

def pick_right_title(df):
	"""
	Takes a df from the rotten_ids.csv and shows the results from the rt string search.
	Borrows heavily from grab_rt_info, with the exception that it does not only return the first entry.
	"""

	api_key = 'beg2csvf5vv2d45tfdqfgegr'
	url_begin = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?q="
	url_end = "&page_limit=20&page=1&apikey=" ##Needs to be changed so it returns more than 1 entry
	
	for i in df.index:
		
		title = df['Clean_Script_Title'].ix[i]
		c_title = title_transform(title)
	
		url = url_begin + c_title + url_end + api_key
	
		page = json.loads(urllib2.urlopen(url).read())
	
		movies = page['movies']
		
		if len(movies) == 0:
			print "No Movies for this name"
			continue
		
		else:
			for m in movies:
				print "Target Movie Name is: " + title
				print "Current Dictionary is: "
				print m
				print "Title: " + str(m['title'])
				print "Year: " + str(m['release_dates'])
				print "Cast: " + str(m['abridged_cast'])
				entry = raw_input('is this correct?')
				if entry == 'y' or entry == 'yes':
					df['rt_id'].ix[i] = m['id']
					break
				elif entry == 'b':
					sys.exit(0)
	
	
	
	
	
	
	