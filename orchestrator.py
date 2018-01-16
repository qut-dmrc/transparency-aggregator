""" This class develops generic methods to create the list of dicts of transparency data
	and upload them to Google BigQuery.
	
	Most of these methods will need to be overwritten to handle specific reporting formats.
	 
"""
import logging
import urllib

import pandas as pd

from csv_reader import CSVReader
from desired_columns_mutator import DesiredColumnsMutator
from downloader import Downloader
from multi_columns_checker import MultiColumnsChecker


class Orchestrator:
    def __init__(self):
        self.df_out = pd.DataFrame()
        self.downloader = Downloader()

    def read_csv(self, filename):
        reader = CSVReader()
        return reader.read(filename)

    def process_with_check(self, df, start_date, end_date):
        checker = MultiColumnsChecker({'expected_source_columns_array': [self.expected_source_columns()]})
        checker.check(df)
        return self.process(df, start_date, end_date)

    def process(self, start_date, end_date):
        raise NotImplementedError()

    def expected_source_columns(self):
        raise NotImplementedError()

    @staticmethod
    def coerce_df(df):
        """ Ensure the final dataframe contains all and only the columns we need. """
        mutator = DesiredColumnsMutator({'desired_columns': ['report_start', 'report_end', 'platform', 'property',
                                                             'country', 'request_type', 'request_subtype',
                                                             'num_requests', 'num_complied', 'num_affected', 'agency',
                                                             'reason']})
        return mutator.mutate(df)

    def process_urls(self, available_urls):
        for data in available_urls:
            url = data['url']
            start_date = data['start_date']
            end_date = data['end_date']

            try:
                src_file = self.downloader.download(url, 'source')
                df = self.read_csv(src_file)
                # logging.info("Processing government requests for {}".format(url))
                # TODO Assert column name changes
                self.process_with_check(df, start_date=start_date, end_date=end_date)
            except urllib.error.URLError as e:
                logging.error("Unable to fetch url: {}. Error: {}".format(url, e))

        return self.coerce_df(self.df_out)
