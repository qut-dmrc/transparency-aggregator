""" Fetch and read Twitter transparency data """
import datetime

import numpy as np

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.semiannual_url_source import SemiannualUrlSource


class TransTwitterInfo(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        df.query('country != "TOTAL"', inplace=True)

        utils.df_strip_char(df, 'percentage where some information produced', '%')
        utils.df_strip_char(df, 'account information requests', '*')

        numeric_cols = ['account information requests', 'percentage where some information produced',
                        'accounts specified']

        df = df.replace('-', np.NaN)  # treat dashs as null, per nic 2018-01-11

        utils.df_convert_to_numeric(df, numeric_cols)

        builder = DataFrameBuilder(df_in=df, platform='Twitter', platform_property='Twitter',
                                   report_start=report_start, report_end=report_end)

        utils.df_convert_from_percentage(df, 'percentage where some information produced',
                                         'account information requests', 'number where some information produced')

        # Extract requests for user data from governments:
        builder.extract_columns(
            request_type='requests for user data',
            request_subtype='all',
            num_requests_col='account information requests',
            num_accounts_specified_col='accounts specified',
            num_requests_complied_col='number where some information produced'
        )

        df_out = builder.get_df()
        return df_out

    def fetch_all(self):
        # Twitter transparency reports are in half-years, starting from 2012-H1
        # "https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-jan-jun-2012.csv"

        start_year = 2012
        end_year = datetime.datetime.utcnow().year

        available_urls = self.get_urls(start_year, end_year)

        df_out = self.process_urls(available_urls)

        return df_out

    def get_urls(self, start_year, end_year):
        source = SemiannualUrlSource(
            {
                "url_template": "https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-$start_month-$end_month-$report_year.csv",
                "start_year": start_year, "end_year": end_year})

        return source.get()

    def expected_source_columns_array(self):
        return [[
            "TIME PERIOD", "COUNTRY", "ISO CODE", "ACCOUNT INFORMATION REQUESTS",
            "PERCENTAGE WHERE SOME INFORMATION PRODUCED",
            "ACCOUNTS SPECIFIED", "FLAGS", "LINKS", "REPORT LINKS",
        ]]
