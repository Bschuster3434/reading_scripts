import csv
import pandas as pd

def open_meta_links():
	return pd.read_csv('meta_links_id.csv', names = ['id', 'page_link', 'downloaded_bool'])
	
def mark_completed(file, id):
	new_rows = []
	
	with open(file, 'rb') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			if int(row[0]) in id:
				row[2] = 1
			new_rows.append(row)
	
	with open(file, 'wb') as csv_file2:
		writer = csv.writer(csv_file2)
		writer.writerows(new_rows)


		