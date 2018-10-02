""" Fetch and read Twitter transparency data - Government removal requests """
import datetime

import numpy as np

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.semiannual_url_source import SemiannualUrlSource


class TransTwitterRemoval(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        df.query('country != "TOTAL"', inplace=True)

        # TODO - figure out what to do with nulls in the source data, because they are almost certainly zeroes

        col_map = {
            'removal requests govt agency police other': 'removal requests government agency police other',
        }

        df.rename(columns=col_map, inplace=True)

        utils.df_strip_char(df, 'percentage where some content withheld', '%')

        numeric_cols = ['removal requests court orders',
                'removal requests government agency police other',
                'percentage where some content withheld', 'accounts specified',
                'accounts withheld', 'tweets withheld', 'accounts tos',
                'accounts no action']

        df = df.replace('-', np.NaN)  # treat dashs as null, per nic 2018-01-11

        utils.df_convert_to_numeric(df, numeric_cols)

        builder = DataFrameBuilder(df_in=df, platform='Twitter', platform_property='Twitter',
                                   report_start=report_start, report_end=report_end)

        df['removal requests'] = df['removal requests court orders'] + df['removal requests government agency police other']

        utils.df_convert_from_percentage(df, pc_col='percentage where some content withheld',
                                         total_col='removal requests', dest_col='number where some content withheld')

        # Extract requests for content removal from governments:
        builder.extract_columns(
            request_type='removal requests',
            request_subtype='all',
            num_requests_col='removal requests',
            num_accounts_specified_col='accounts specified',
            num_requests_complied_col='number where some content withheld',
            num_accounts_suspended_col='accounts withheld',
            num_content_removed_col='tweets withheld',
        )

        df_out = builder.get_df()
        return df_out

    def fetch_all(self):
        # Twitter transparency reports are in half-years, starting from 2012-H1
        # https://transparency.twitter.com/content/dam/transparency-twitter/data/download-removal-requests/removal-requests-report-jul-dec-2017.csv

        start_year = 2012
        end_year = datetime.datetime.utcnow().year

        available_urls = self.get_urls(start_year, end_year)

        df_out = self.process_urls(available_urls)

        return df_out

    def get_urls(self, start_year, end_year):
        source = SemiannualUrlSource(
            {
                "url_template": "https://transparency.twitter.com/content/dam/transparency-twitter/data/download-removal-requests/removal-requests-report-$start_month-$end_month-$report_year.csv",
                "start_year": start_year, "end_year": end_year})

        return source.get()

    def expected_source_columns_array(self):
        return [
            ["COUNTRY", "LINKS", "TIME PERIOD", "ISO CODE", "REPORT LINKS", "FLAGS", "ACCOUNTS SPECIFIED",
             "ACCOUNTS WITHHELD", "TWEETS WITHHELD", "REMOVAL REQUESTS (COURT ORDERS)",
             "REMOVAL REQUESTS (GOVERNMENT AGENCY, POLICE, OTHER) ", "ACCOUNTS (NO ACTION)",
             "PERCENTAGE WHERE SOME CONTENT WITHHELD", "ACCOUNTS (TOS)",],

            ["COUNTRY", "LINKS", "TIME PERIOD", "ISO CODE", "REPORT LINKS", "FLAGS", "ACCOUNTS SPECIFIED",
            "ACCOUNTS WITHHELD", "TWEETS WITHHELD", "REMOVAL REQUESTS (COURT ORDERS)",
            "REMOVAL REQUESTS (GOV’T AGENCY, POLICE, OTHER)", "ACCOUNTS (NO ACTION)",
            "PERCENTAGE WHERE SOME CONTENT WITHHELD", "ACCOUNTS (TOS)",],
        ]
