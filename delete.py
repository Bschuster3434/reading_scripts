import pandas as pd

w_file = 'writers.csv'
g_file = 'genres.csv'
s_file = 'script.csv'

def delete_id_instance(id , w = w_file, g = g_file, s = s_file):
	
	delete_individual_csv_id(id, w)
	delete_individual_csv_id(id, g)
	delete_individual_csv_id(id, s)
	
	print "Deleted " + str(id) + " from write, genre and script."

	
def delete_individual_csv_id(id, file):
	df = pd.read_csv(file)
	df = df[df.Script_Id != int(id)]
	df.to_csv( file, index = False )