""" This class develops generic methods to create the list of dicts of transparency data
    and upload them to Google BigQuery.
    
    Most of these methods will need to be overwritten to handle specific reporting formats.
     
"""
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, date
import logging


class TransparencyAggregator:
    def __init__(self):
        self.df = None 
        self.df_out = pd.DataFrame()

    def read_csv(self, filename_or_url):
        self.df = pd.read_csv(filename_or_url, encoding="UTF-8")
        logging.debug("Found {} rows.".format(self.df.shape[0]))

    def process(self, start_date, end_date):
        return self.df

    @staticmethod
    def coerce_df(df):
        """ Ensure the final dataframe contains all and only the columns we need. """

        columns = ['report_start', 'report_end', 'platform', 'property', 'country', 'request_type', 'num_requests',
                   'num_complied', 'num_affected', 'agency', 'reason']

        for col in columns:
            if col not in df.columns:
                df[col] = None

        df = df[columns]

        return df

    


