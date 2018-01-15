""" 
"""
import json
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, date
import numpy as np
import logging
import urllib
from downloader import Downloader

from csv_reader import CSVReader
import utils
from mutator import Mutator

class DesiredColumnsMutator(Mutator):
	def in_place_mutate(self, df):
		""" Ensure the dataframe contains all and only the columns we need. """
		columns = self.config['desired_columns']

		for col in columns:
			if col not in df.columns:
				df[col] = None

		df = df[columns]
		return df
