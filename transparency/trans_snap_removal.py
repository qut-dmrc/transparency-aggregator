""" Fetch and read Snap transparency data """
import datetime

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.semiannual_url_source import SemiannualUrlSource
from transparency.snap_reader import SnapReader


class TransSnapRemoval(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        """['country', 'removal requests', 'percentage of requests where some content was removed'],
        """

        col_map = {
            'percentage of requests where some content was removed': 'percent removal requests complied',
        }

        # TODO - figure out what to do with nulls in the source data, because they are almost certainly zeroes
        df.columns = [ utils.strip_punctuation(x.lower()) for x in df.columns.values ]
        df.rename(columns=col_map, inplace=True)

        utils.df_strip_char(df, 'percent removal requests complied', '%')

        # convert strings to numbers
        numeric_cols = [
            'removal requests',
            'percent removal requests complied',
        ]

        utils.df_convert_to_int(df, numeric_cols)

        utils.df_percentage_to_count(df, 'percent removal requests complied', 'removal requests', 'removal requests complied')

        builder = DataFrameBuilder(df_in=df, platform='Snap', platform_property='Snapchat',
                                   report_start=report_start, report_end=report_end)


        # Extract removal requests from governments:
        builder.extract_columns(
            request_type='content restrictions',
            request_subtype='all',
            num_requests_col='removal requests',
            num_accounts_specified_col='',
            num_requests_complied_col='removal requests complied',
        )

        # Check that the date passed in matches the date in the table
        date_start_mismatch = ((report_start == df['report start from table']) | (report_start == '')).all()
        date_end_mismatch = ((report_end == df['report end from table']) | (report_end == '')).all()
        utils.check_assumption(date_start_mismatch, "Start dates in table did not match dates passed in.")
        utils.check_assumption(date_end_mismatch, "End dates in table did not match dates passed in.")

        df_out = builder.get_df()
        df_out['reportstart'] = df_out['report start from table']
        df_out['reportend'] = df_out['report end from table']

        return df_out

    def expected_source_columns_array(self):
        cols = [
            ['country', 'removal requests', 'percentage of requests where some content was removed',
             'report start from table', 'report end from table'],
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
        return reader.read(filename, "Governmental Content Removal Requests")
