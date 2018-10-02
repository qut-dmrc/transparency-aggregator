""" Fetch and read Twitter transparency data """
import logging

import pandas as pd

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.static_source import StaticSource
from transparency.zip_csv_reader import ZipCSVReader


class TransGoogleInfo(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        numeric_cols = ['user data requests', 'percentage of requests where some data produced',
                        'usersaccounts specified']

        utils.df_convert_to_numeric(df, numeric_cols)

        builder = DataFrameBuilder(df_in=df, platform='Google', platform_property='Google',
                                   report_start='', report_end='')

        utils.df_convert_from_percentage(df, 'percentage of requests where some data produced', 'user data requests',
                                         'number where some information produced')

        def get_request_type(row):
            legal = row['legal process']
            if legal == 'Preservation Requests':
                return 'preservation requests'
            else:
                return 'requests for user data'

        def get_request_subtype(row):
            legal = row['legal process']
            if legal == 'Preservation Requests':
                return 'all'
            else:
                return legal

        builder.extract_columns(
            request_type=get_request_type,
            request_subtype=get_request_subtype,
            num_requests_col='user data requests',
            num_accounts_specified_col='usersaccounts specified',
            num_requests_complied_col='number where some information produced'
        )

        # Extract requests for user data from governments:

        df_out = builder.get_df()
        df_out['report_end'] = df['period ending'].apply(
            lambda d: utils.str_to_date(d).replace(hour=23, minute=59, second=59))

        df_out['report_start'] = df_out['report_end'].apply(
            lambda report_end: (report_end + pd.DateOffset(days=1) - pd.DateOffset(months=6)).replace(hour=0, minute=0, second=0))

        for report_start in df_out['report_start']:
            utils.check_assumption(report_start.day == 1, "Report Start date should be the first of the month")
            utils.check_assumption(report_start.month in [1, 7], "Report Start month should be January or July")
        return df_out

    def fetch_all(self):
        available_urls = self.get_urls()

        df_out = self.process_urls(available_urls)

        return df_out

    def expected_source_columns_array(self):
        return [['CLDR Territory Code', 'UsersAccounts Specified', 'Country', 'Legal Process',
                 'Percentage of requests where some data produced', 'Period Ending', 'User Data Requests']]

    def get_urls(self):
        source = StaticSource({'data': [{
            "url": "https://storage.googleapis.com/transparencyreport/google-user-data-requests.zip",
            "report_start": '',
            "report_end": '',
        }]})

        return source.get()

    def read(self, filename):
        reader = ZipCSVReader({'internal_filename': 'google-user-data-requests/google-user-data-requests.csv'})
        return reader.read(filename)
