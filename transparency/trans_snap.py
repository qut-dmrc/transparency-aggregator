""" Fetch and read Snap transparency data """
import datetime

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.semiannual_url_source import SemiannualUrlSource
from transparency.snap_reader import SnapReader


class TransSnap(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        """['reporting period', 'emergency requests', 'accounts emergency',
       'percent emergency requests complied', 'other information requests',
       'accounts other', 'percent other requests complied', 'report_start',
       'report_end']
        """

        col_map = {
            'account identifiers* for emergency requests': 'accounts emergency',
            'percentage of emergency requests where some data was produced': 'percent emergency requests complied',
            'account identifiers* for other information requests': 'accounts other',
            'other information requests': 'other requests',
            'percentage of other information requests where some data was produced': 'percent other requests complied',
        }

        # TODO - figure out what to do with nulls in the source data, because they are almost certainly zeroes
        df.columns = df.columns.str.lower()
        df.rename(columns=col_map, inplace=True)

        utils.df_strip_char(df, 'percent emergency requests complied', '%')
        utils.df_strip_char(df, 'percent other requests complied', '%')

        # convert strings to numbers
        numeric_cols = [
            'emergency requests', 'accounts emergency',
            'percent emergency requests complied', 'other requests',
            'accounts other', 'percent other requests complied',
        ]

        utils.df_convert_to_int(df, numeric_cols)

        utils.df_percentage_to_count(df, 'percent emergency requests complied', 'emergency requests', 'emergency requests complied')
        utils.df_percentage_to_count(df, 'percent other requests complied', 'other requests', 'other requests complied')

        builder = DataFrameBuilder(df_in=df, platform='Snap', platform_property='Snapchat',
                                   report_start=report_start, report_end=report_end)


        # Extract requests for user data from governments:
        builder.extract_columns(
            request_type='requests for user data',
            request_subtype='emergency disclosure requests',
            num_requests_col='emergency requests',
            num_accounts_specified_col='accounts emergency',
            num_requests_complied_col='emergency requests complied',
        )

        builder.extract_columns(
            request_type='requests for user data',
            request_subtype='non emergency disclosure requests',
            num_requests_col='other requests',
            num_accounts_specified_col='accounts other',
            num_requests_complied_col='other requests complied',
        )

        # Check that the date passed in matches the date in the table
        date_start_mismatch = ((report_start == df['report_start_from_table']) | (report_start == '')).all()
        date_end_mismatch = ((report_end == df['report_end_from_table']) | (report_end == '')).all()
        utils.check_assumption(date_start_mismatch, "Start dates in table did not match dates passed in.")
        utils.check_assumption(date_end_mismatch, "End dates in table did not match dates passed in.")

        df_out = builder.get_df()
        df_out['report_start'] = df_out['report_start_from_table']
        df_out['report_end'] = df_out['report_end_from_table']

        return df_out

    def expected_source_columns_array(self):
        cols = [
            ['country', 'Emergency Requests',
             'Account Identifiers* for Emergency Requests',
             'Percentage of Emergency Requests where some data was produced',
             'Other Information Requests',
             'Account Identifiers* for Other Information Requests',
             'Percentage of Other Information Requests where some data was produced',
             'report_start_from_table', 'report_end_from_table'],
        ]
        return cols

    def fetch_all(self):
        start_year = 2015  # Snap has partial data for 2014 - Feb 2015 that we are ignoring.
        end_year = datetime.datetime.utcnow().year

        available_urls = self.get_urls(start_year, end_year)

        df_out = self.process_urls(available_urls)

        return df_out

    def get_urls(self, start_year, end_year):
        source = SemiannualUrlSource(
            {"url_template": "https://www.snap.com/en-US/privacy/transparency/$date_end",
             "start_year": start_year, "end_year": end_year})

        # special case for current period - available at https://www.snap.com/en-US/privacy/transparency/

        urls = source.get()

        current_year = {'url': "https://www.snap.com/en-US/privacy/transparency/",
                        'report_start': "", 'report_end': ""}

        urls.append(current_year)

        return urls

    def read(self, filename):
        reader = SnapReader({})
        return reader.read(filename)
