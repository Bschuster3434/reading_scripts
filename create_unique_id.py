import csv

def open_links():	
	with open("script_links.txt", "r") as file:
		data = file.readlines()
		links = [i[:-1] for i in data]
	return links
	
def add_unique_id(links):
	id= 1
	links_list = []
	for meta in links:
		links_list.append([id, meta])
		id = id + 1
	
	return links_list

def write_links_ids():
	links = open_links()
	links_list = add_unique_id(links)
	with open('meta_links_id.csv', 'wb') as file:
		writer = csv.writer(file, delimiter= ',')
		for i in links_list:
			writer.writerow(i)