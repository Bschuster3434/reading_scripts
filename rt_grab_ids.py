import pandas as pd
import json
import urllib2

r_file = 'rotten_ids.csv'

r_df = pd.read_csv('rotten_ids.csv')


def append_info_to_csv(df):

	for i in df.index:
		s_title = df['Script_Title'].ix[i]
		rt_dict = grab_rt_info(s_title)
		print s_title, rt_dict
	

def grab_rt_info(title):
	"""
	This function pulls in all the relevant rotten tomatoes information for each movie.
	Uses the 'Movies Search' api query to movies
	Search Rotten Tomatoes API Documentation for more information
	"""
	api_key = 'beg2csvf5vv2d45tfdqfgegr'
	url_begin = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?q="
	url_end = "&page_limit=1&page=1&apikey="
	
	c_title = title_transform(title)
	
	url = url_begin + c_title + url_end + api_key
	
	page = json.loads(urllib2.urlopen(url).read())
	
	if page['total'] == 0:
		return None
	
	movie_info = {}
	
	movie = page['movies'][0]
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
	
	
