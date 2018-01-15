"""
Read a CSV into a data frame
"""
import re
import urllib
import urllib.request
import os.path
import logging
import pandas as pd
import numpy as np

class CSVReader:
	def read(self, filename):
		df = pd.read_csv(filename, encoding="UTF-8", dtype=np.object_)  #force dtype to avoid columns changing type because sometimes they have *s in them
		logging.debug("Found {} rows.".format(df.shape[0]))
		return df
