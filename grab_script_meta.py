import urllib2
from BeautifulSoup import BeautifulSoup

def grab_script_meta(meta_url):
	soup = BeautifulSoup( urllib2.urlopen( meta_url ) )
	script_details_table = get_script_details_table(soup)
	
	writer_genre_scripts = script_details_table.findAll('a')
	
	writers = [ i.contents[0] for i in writer_genre_scripts if i['href'].find('writer') != -1]
	genres = [ i.contents[0] for i in writer_genre_scripts if i['href'].find('genre') != -1]
	script_url = "http://www.imsdb.com/" + [ i.get('href') for i in writer_genre_scripts if i['href'].find('scripts') != -1][0]
	
	sdt_string = str(script_details_table)
	
	script_date = grab_string_details("Script Date", sdt_string)
	movie_release_date = grab_string_details("Movie Release Date", sdt_string)
	
	return {'writers' : writers, 'genres' : genres, 'script_url' : script_url, 'script_date' : script_date, 'movie_release_date' : movie_release_date}
	
	

def grab_string_details(begin_search, string):
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
	
	all_tables = soup.findAll('table')

	for i in all_tables:
		try:
			result = i['class'] == 'script-details'
		except KeyError:
			continue
		if result == True:
			return i



def open_links():	
	with open("script_links.txt", "r") as file:
		data = file.readlines()
		links = [i[:-1] for i in data]
	return links
