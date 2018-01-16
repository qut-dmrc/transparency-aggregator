""" Fetch and read Twitter transparency data """
import logging
from zipfile import ZipFile

import numpy as np
import pandas as pd

import utils
from data_frame_builder import DataFrameBuilder
from orchestrator import Orchestrator


class TransGoogle(Orchestrator):

    def process(self, df, start_date, end_date):
        # Rename the columns to a standard format, and account for changes over the years
        df.columns = df.columns.str.lower()
        utils.df_fix_columns(df)

        # delete TOTAL country

        numeric_cols = ['user data requests', 'percentage of requests where some data produced',
                        'users/accounts specified']

        utils.df_convert_to_numeric(df, numeric_cols)

        builder = DataFrameBuilder(df_in=df, df_out=self.df_out, platform='Google', platform_property='Google',
                                   report_start='', report_end='')

        utils.df_convert_from_percentage(df, 'percentage of requests where some data produced', 'user data requests',
                                         'number where some information produced')

        # Extract requests for user data from governments:
        builder.extract_columns('requests for user data', '!!',
                                'user data requests', 'users/accounts specified',
                                'number where some information produced')

        # Extract content restriction requests:
        #		builder.extract_columns('content restrictions', 'content restrictions', 'content_num_affected', 'content_num_complied')

        # Extract account preservation requests
        #		builder.extract_columns('preservation requests',
        #							 'preservations requested', 'preservations_num_affected', 'users / accounts preserved')

        self.df_out = builder.get_df()
        self.df_out['report_end'] = df['period ending'].apply(utils.str_to_date)

        self.df_out['report_start'] = self.df_out['report_end'].apply(
            lambda report_end: (report_end + pd.DateOffset(days=1) - pd.DateOffset(months=6)))

        for report_start in self.df_out['report_start']:
            utils.check_assumption(report_start.day == 1, "Report Start date should be the first of the month")
            utils.check_assumption(report_start.month in [1, 7], "Report Start month should be January or July")
        return self.df_out

    def fetch_all(self):
        # Twitter transparency reports are in half-years, starting from 2012-H1
        # "https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-jan-jun-2012.csv"

        available_urls = self.get_urls()

        self.df_out = self.process_urls(available_urls)

        return self.df_out

    def expected_source_columns_array(self):
        return [['CLDR Territory Code', 'Users/Accounts Specified', 'Country', 'Legal Process',
                'Percentage of requests where some data produced', 'Period Ending', 'User Data Requests']]

    def get_urls(self):
        data = []

        url = "https://storage.googleapis.com/transparencyreport/google-user-data-requests.zip"

        period_data = {'url': url, 'start_date': '', 'end_date': ''}

        data.append(period_data)

        return data

    def read_csv(self, filename_or_url):
        with ZipFile(filename_or_url) as zipf:
            with zipf.open('google-user-data-requests/google-user-data-requests.csv') as data_file:
                df = pd.read_csv(data_file, encoding="UTF-8",
                                 dtype=np.object_)  # force dtype to avoid columns changing type because sometimes they have *s in them
                logging.debug("Found {} rows.".format(df.shape[0]))
                return df
