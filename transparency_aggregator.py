""" This class develops generic methods to create the list of dicts of transparency data
	and upload them to Google BigQuery.
	
	Most of these methods will need to be overwritten to handle specific reporting formats.
	 
"""
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, date
import numpy as np
import logging
import urllib
from downloader import Downloader


class TransparencyAggregator:
	def __init__(self):
		self.df_out = pd.DataFrame()
		self.downloader = Downloader()

	def read_csv(self, filename_or_url):
		df = pd.read_csv(filename_or_url, encoding="UTF-8", dtype=np.object_)  #force dtype to avoid columns changing type because sometimes they have *s in them
		logging.debug("Found {} rows.".format(df.shape[0]))
		return df

	def process(self, start_date, end_date):
		return None

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
				self.process(df, start_date=start_date, end_date=end_date)
			except urllib.error.URLError as e:
				logging.error("Unable to fetch url: {}. Error: {}".format(url, e))
				
		return self.coerce_df(self.df_out)
	


