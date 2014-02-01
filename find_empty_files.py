import pandas as pd
import numpy as np
import os

dir_path = "raw_script/"

def find_file_size(file):
	return os.stat(file).st_size
