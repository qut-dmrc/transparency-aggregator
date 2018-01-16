""" Fetch and read Twitter transparency data """
import datetime

import numpy as np

import utils
from data_frame_builder import DataFrameBuilder
from orchestrator import Orchestrator


class TransTwitter(Orchestrator):

    def process(self, df, start_date, end_date):

        # Rename the columns to a standard format, and account for changes over the years
        df.columns = df.columns.str.lower()
        utils.df_fix_columns(df)

        # delete TOTAL country

        utils.df_strip_char(df, 'percentage where some information produced', '%')
        utils.df_strip_char(df, 'account information requests', '*')

        numeric_cols = ['account information requests', 'percentage where some information produced',
                        'accounts specified']

        df = df.replace('-', np.NaN)  # treat dashs as null, per nic 2018-01-11

        utils.df_convert_to_numeric(df, numeric_cols)

        builder = DataFrameBuilder(df_in=df, df_out=self.df_out, platform='Twitter', platform_property='Twitter',
                                   report_start=start_date, report_end=end_date)

        utils.df_convert_from_percentage(df, 'percentage where some information produced',
                                         'account information requests', 'number where some information produced')

        # Extract requests for user data from governments:
        builder.extract_columns('requests for user data', 'all',
                                'account information requests', 'accounts specified',
                                'number where some information produced')

        # Extract content restriction requests:
        #		builder.extract_columns('content restrictions', 'content restrictions', 'content_num_affected', 'content_num_complied')

        # Extract account preservation requests
        #		builder.extract_columns('preservation requests',
        #							 'preservations requested', 'preservations_num_affected', 'users / accounts preserved')

        self.df_out = builder.get_df()
        return self.df_out

    def fetch_all(self):
        # Twitter transparency reports are in half-years, starting from 2012-H1
        # "https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-jan-jun-2012.csv"

        start_year = 2012
        end_year = datetime.datetime.utcnow().year

        available_urls = self.get_urls(start_year, end_year)

        self.df_out = self.process_urls(available_urls)

        return self.df_out

    def get_urls(self, start_year, end_year):
        data = []

        for report_year in range(start_year, end_year + 1):

            for period, start_month, end_month in [("H1", "jan", "jun"), ("H2", "jul", "dec")]:
                url = f"https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-{start_month}-{end_month}-{report_year}.csv"
                if period == 'H1':
                    start_date = "{}-01-01 00:00:00".format(report_year)
                    end_date = "{}-06-30 23:59:59".format(report_year)
                else:
                    start_date = "{}-07-01 00:00:00".format(report_year)
                    end_date = "{}-12-31 23:59:59".format(report_year)

                period_data = {'url': url, 'start_date': start_date, 'end_date': end_date}

                data.append(period_data)

        return data

    def expected_source_columns_array(self):
        return [[
            "TIME PERIOD", "COUNTRY", "ISO CODE", "ACCOUNT INFORMATION REQUESTS", "PERCENTAGE WHERE SOME INFORMATION PRODUCED",
            "ACCOUNTS SPECIFIED", "FLAGS", "LINKS", "REPORT LINKS",
        ]]
