""" Fetch and read Twitter transparency data """
import logging

import pandas as pd

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.static_source import StaticSource
from transparency.zip_csv_reader import ZipCSVReader


class TransGoogleRemoval(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        # Google does not report removal requests from some countries where the number is low.
        # This is signified by '<10' in number of requests column
        # And sometimes, Google reports '?' in the number of requests column.
        # We ignore all of these values.
        df = df[~(df['all requests: number of requests'] == '<10')]
        df = df[~(df['all requests: number of requests'] == '?')]

        numeric_cols = ['all requests number of requests',
                        'all requests fully or partially complied with',
                        'all requests items requested to be removed',
                        'court orders number of requests', 'court orders fully or partially complied with',
                        'court orders items requested to be removed',
                        'other requests executive police etc number of requests',
                        'other requests executive police etc fully or partially complied with',
                        'other requests executive police etc items requested to be removed', ]

        utils.df_convert_to_numeric(df, numeric_cols)

        builder = DataFrameBuilder(df_in=df, platform='Google', platform_property='Google',
                                   report_start='', report_end='')

        utils.df_convert_from_percentage(df, 'all requests: % fully or partially complied with', 'all requests: number of requests',
                                         'all requests: number where some content removed')

        builder.extract_columns(
            request_type='removal requests',
            request_subtype='all',
            num_requests_col='all requests: number of requests',
            num_content_specified_col='all requests: items requested to be removed',
            num_requests_complied_col='all requests: number where some content removed'
        )

        # Extract requests for user data from governments:

        df_out = builder.get_df()
        df_out['report_end'] = df['period ending'].apply(
            lambda d: utils.str_to_date(d).replace(hour=23, minute=59, second=59))

        df_out['report_start'] = df_out['report_end'].apply(
            lambda report_end: (report_end + pd.DateOffset(days=1) - pd.DateOffset(months=6)).replace(hour=0, minute=0,
                                                                                                      second=0))

        for report_start in df_out['report_start']:
            utils.check_assumption(report_start.day == 1, "Report Start date should be the first of the month")
            utils.check_assumption(report_start.month in [1, 7], "Report Start month should be January or July")
        return df_out

    def fetch_all(self):
        available_urls = self.get_urls()

        df_out = self.process_urls(available_urls)

        return df_out

    def expected_source_columns_array(self):
        return [['Period Ending', 'Country', 'CLDR Territory Code', 'All Requests: Number of Requests',
                 'All Requests: % Fully Or Partially Complied With', 'All Requests: Items Requested To Be Removed',
                 'Court Orders: Number of Requests', 'Court Orders: % Fully Or Partially Complied With',
                 'Court Orders: Items Requested To Be Removed',
                 'Other Requests (Executive, Police, etc.): Number of Requests',
                 'Other Requests (Executive, Police, etc.): % Fully Or Partially Complied With',
                 'Other Requests (Executive, Police, etc.): Items Requested To Be Removed',
                 ]]

    def get_urls(self):
        source = StaticSource({'data': [{
            "url": "https://storage.googleapis.com/transparencyreport/google-government-removals.zip",
            "report_start": '',
            "report_end": '',
        }]})

        return source.get()

    def read(self, filename):
        reader = ZipCSVReader(
            {'internal_filename': 'google-government-removals/google-government-removal-requests.csv'})
        return reader.read(filename)
