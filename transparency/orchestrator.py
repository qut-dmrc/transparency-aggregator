""" This class develops generic methods to create the list of dicts of transparency data
	and upload them to Google BigQuery.
	
	Most of these methods will need to be overwritten to handle specific reporting formats.
	 
"""
import logging
import os
import urllib

import pandas as pd

from transparency import utils
from transparency.csv_reader import CSVReader
from transparency.desired_columns_mutator import DesiredColumnsMutator
from transparency.downloader import Downloader
from transparency.multi_columns_checker import MultiColumnsChecker


class Orchestrator:
    def __init__(self):
        self.df_out = pd.DataFrame()
        self.downloader = Downloader()

    def name(self):
        return type(self).__name__

    def read(self, filename):
        reader = CSVReader({})
        return reader.read(filename)

    def process_with_check(self, df, report_start, report_end):
        checker = MultiColumnsChecker({'expected_source_columns_array': self.expected_source_columns_array()})
        checker.check(df)
        return self.process(df, report_start, report_end)

    def process(self, report_start, report_end):
        raise NotImplementedError()

    def expected_source_columns(self):
        raise NotImplementedError()

    @staticmethod
    def coerce_df(df):
        """ Ensure the final dataframe contains all and only the columns we need. """
        mutator = DesiredColumnsMutator({'desired_columns': [
            'report_start',
            'report_end',
            'platform',
            'property',
            'country',
            'request_type',
            'request_subtype',
            'num_requests',
            'num_accounts_specified',
            'num_requests_complied',
            'num_accounts_complied',
            'agency',
            'reason'
        ]})
        return mutator.mutate(df)

    def process_urls(self, available_urls):
        for data in available_urls:
            url = data['url']
            report_start = data.get('report_start', None)
            report_end = data.get('report_end', None)

            try:
                # note two dirnames, to go up a directory
                src_file = self.downloader.download(url, utils.make_path('cache'))
                df = self.read(src_file)
                self.process_with_check(df, report_start=report_start, report_end=report_end)
            except urllib.error.URLError as e:
                logging.error("Unable to fetch url: {}. Error: {}".format(url, e))

        return self.coerce_df(self.df_out)
