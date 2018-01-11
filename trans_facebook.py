""" Fetch and read Facebook transparency data """
import datetime
import logging
import urllib
import numpy as np
import pandas as pd

from transparency_aggregator import TransparencyAggregator
from data_frame_builder import DataFrameBuilder

class FB(TransparencyAggregator):

	def process(self, start_date, end_date):

		# Rename the columns to a standard format, and account for changes over the years
		self.df.columns = self.df.columns.str.lower()

		col_map = {
			'requests for user data': 'total requests for user data',
			'user accounts referenced': 'total user accounts referenced',
			'percentage of requests where some data produced': 'total percentage of requests where some data produced',
		}

		self.df.rename(columns=col_map, inplace=True)

		# Convert percentages to numbers
		self.df['total percentage of requests where some data produced'] = self.df[
			'total percentage of requests where some data produced'].str.rstrip('%')

		#		self.df['number of requests where some data produced'] = self.df.apply(convert_percentages, axis=1)

		# convert strings to numbers
		numeric_cols = ['total requests for user data', 'total user accounts referenced',
						'total percentage of requests where some data produced', 'content restrictions',
						'content_num_affected', 'content_num_complied', 'preservations requested',
						'preservations_num_affected', 'users / accounts preserved']

		for col in numeric_cols:
			if col not in self.df.columns:
				self.df[col] = None
			else:
				if self.df[col].dtype == np.object_:
					# replace formatting commas
					self.df[col] = self.df[col].str.replace(',', '')

					# replace ranges with the lower bound of the range
					self.df[col] = self.df[col].str.replace(r"(\d+)( - )(\d+)", r'\1')

					self.df[col] = pd.to_numeric(self.df[col], errors='raise')

		self.df['number of requests where some data produced'] = self.df[
																	 'total percentage of requests where some data produced'] * \
																 self.df['total requests for user data'] / 100.0
		self.df['number of requests where some data produced'] = self.df[
			'number of requests where some data produced'].round()
		# this doesn't seem to work: .astype(int, errors='ignore')
		
		self.df['preservations_num_affected'] = self.df[
			'preservations requested']  # Assume 1:1 mapping on requests:accounts

		builder = DataFrameBuilder(df_in = self.df, df_out = self.df_out, platform = 'Facebook', platform_property = 'Facebook', 
									report_start = start_date, report_end = end_date)

		# Extract requests for user data from governments:
		builder.extract_columns('requests for user data',
								'total requests for user data', 'total user accounts referenced',
								'number of requests where some data produced')

		# Extract content restriction requests:
		builder.extract_columns('content restrictions', 'content restrictions', 'content_num_affected', 'content_num_complied')

		# Extract account preservation requests
		builder.extract_columns('preservation requests',
							 'preservations requested', 'preservations_num_affected', 'users / accounts preserved')

		self.df_out = builder.get_df()
		return self.df_out

	def fetch_all(self):
		# Facebook transparency reports are in half-years, starting from 2013-H1
		# "https://transparency.facebook.com/download/2013-H1/"
		
		start_year = 2013
		end_year = datetime.datetime.utcnow().year
		
		available_urls = self._get_urls(start_year, end_year)
		
		self.df_out = self._process_urls(available_urls)

		return self.df_out

	def _get_urls(self, start_year, end_year):
		data = []

		for report_year in range(start_year, end_year + 1):

			for period in ('H1', 'H2'):
				url = "https://transparency.facebook.com/download/{}-{}/".format(report_year, period)
				if period == 'H1':
					start_date = "{}-01-01 00:00:00".format(start_year)
					end_date = "{}-06-30 23:59:59".format(start_year)
				else:
					start_date = "{}-07-01 00:00:00".format(start_year)
					end_date = "{}-12-31 23:59:59".format(start_year)

				period_data = { 'url': url, 'start_date': start_date, 'end_date': end_date }

				data.append(period_data)

		return data

	def _process_urls(self, available_urls):
		for data in available_urls:
			url = data['url']
			start_date = data['start_date']
			end_date = data['end_date']

			logging.info("Fetching FB transparency report from {}".format(url))

			try:
				self.read_csv(url)
				logging.info("Processing government requests for {}".format(url))
				self.process(start_date=start_date, end_date=end_date)
			except urllib.error.HTTPError as e:
				logging.error("Unable to fetch url: {}. Error: {}".format(url, e))
				
		return self.coerce_df(self.df_out)

def convert_percentages(row): #TODO Move to util
	num_complied = None
	try:
		num_complied = float(row['total percentage of requests where some data produced'].rstrip(
			'%'))
		num_complied = num_complied * row['total requests for user data'] / 100.0
		num_complied = int(num_complied)
	except Exception as e:
		logging.error(
			"Unable to convert row to integer - expected percentage. Value: {}; Error: {}".format(num_complied, e))
		pass

	return num_complied

