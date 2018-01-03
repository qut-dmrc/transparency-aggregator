""" This class develops generic methods to create the list of dicts of transparency data
    and upload them to Google BigQuery.
    
    Most of these methods will need to be overwritten to handle specific reporting formats.
     
"""
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, date
import logging


class TransparencyAggregator():
    def __init__(self):
        self.df = None
        self.df_out = pd.DataFrame()

    def read_csv(self, filename_or_url):
        self.df = pd.read_csv(filename_or_url, encoding="UTF-8")
        logging.debug("Found {} rows.".format(self.df.shape[0]))

    def process(self, start_date, end_date):
        return self.df

    def coerce_df(self, df):
        """ Ensure the final dataframe contains all and only the columns we need. """

        columns = ['report_start', 'report_end', 'platform', 'property', 'country', 'request_type', 'num_requests',
                   'num_complied', 'num_affected']

        for col in columns:
            if col not in df.columns:
                df[col] = None

        df = df[columns]

        return df


    def extract_columns(self, df, platform, property, report_start, report_end, request_type, num_requests_col, num_affected_col, num_complied_col, jurisdiction_col='country'):
        """ Take a dataframe with the columns num_requested and num_complied_col
            and return a new dataframe in our normal form format.
        """

        report_start = c_to_date(report_start)
        report_end = c_to_date(report_end)

        df_out = df[[jurisdiction_col, num_requests_col, num_complied_col, num_affected_col]].copy()
        df_out['platform'] = platform
        df_out['property'] = property
        df_out['report_start'] = report_start
        df_out['report_end'] = report_end
        df_out['request_type'] = request_type

        col_map = {num_complied_col: 'num_complied',
                       num_requests_col: 'num_requests',
                   num_affected_col: 'num_affected'
                   }

        df_out.rename(columns=col_map, inplace=True)

        self.df_out = self.df_out.append(df_out)

        return self.df_out

def c_to_date(date_in):
    """ Simple method to convert a string to a date. If passed a date, leave as is. """
    if isinstance(date_in, str):
        return parse(date_in)
    elif isinstance(date_in, (datetime, date)):
        return date_in
    else:
        raise ValueError("Input not in a string or date format. Got: {}".format(date_in))

