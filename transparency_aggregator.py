""" This class develops generic methods to create the list of dicts of transparency data
	and upload them to Google BigQuery.
	
	Most of these methods will need to be overwritten to handle specific reporting formats.
	 
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

class TransparencyAggregator:
	def __init__(self):
		self.df_out = pd.DataFrame()
		self.downloader = Downloader()

	def read_csv(self, filename):
		reader = CSVReader()
		return reader.read(filename)
		


	def process_with_check(self, df, start_date, end_date):
		expected_cols = set(self.expected_source_columns())
		actual_cols = set(df.columns.values)
		extra_cols = list(actual_cols - expected_cols)
		missing_cols = list(expected_cols - actual_cols)

		utils.check_assumption(len(extra_cols) == 0, "Unexpected extra columns: " + json.dumps(extra_cols))
		utils.check_assumption(len(missing_cols) == 0, "Unexpected missing columns: " + json.dumps(missing_cols))

		return self.process(df, start_date, end_date)

	def process(self, start_date, end_date):
		raise NotImplementedError()

	def expected_source_columns(self):
		raise NotImplementedError()

	@staticmethod
	def coerce_df(df):
		""" Ensure the final dataframe contains all and only the columns we need. """

		columns = ['report_start', 'report_end', 'platform', 'property', 'country', 'request_type', 'request_subtype', 'num_requests',
				   'num_complied', 'num_affected', 'agency', 'reason']

		for col in columns:
			if col not in df.columns:
				df[col] = None

		df = df[columns]

		return df

	def process_urls(self, available_urls):
		for data in available_urls:
			url = data['url']
			start_date = data['start_date']
			end_date = data['end_date']


			try:
				src_file = self.downloader.download(url, 'source')
				df = self.read_csv(src_file)
				#logging.info("Processing government requests for {}".format(url))
				# TODO Assert column name changes
				self.process_with_check(df, start_date=start_date, end_date=end_date)
			except urllib.error.URLError as e:
				logging.error("Unable to fetch url: {}. Error: {}".format(url, e))
				
		return self.coerce_df(self.df_out)
	


