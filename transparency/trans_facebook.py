""" Fetch and read Facebook transparency data """
import datetime

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.semiannual_url_source import SemiannualUrlSource


class FB(Orchestrator):

    def process(self, df, report_start, report_end):

        # Rename the columns to a standard format, and account for changes over the years
        df.columns = df.columns.str.lower()
        utils.df_fix_columns(df)

        col_map = {
            'requests for user data': 'total requests for user data',
            'user accounts referenced': 'total user accounts referenced',
            'percentage of requests where some data produced': 'total percentage of requests where some data produced',
        }

        df.rename(columns=col_map, inplace=True)

        utils.df_strip_char(df, 'total percentage of requests where some data produced', '%')

        # convert strings to numbers
        numeric_cols = ['total requests for user data', 'total user accounts referenced',
                        'total percentage of requests where some data produced', 'content restrictions',
                        'content_num_affected', 'content_num_complied', 'preservations requested',
                        'preservations_num_affected', 'users / accounts preserved']

        utils.df_convert_to_numeric(df, numeric_cols)

        df['number of requests where some data produced'] = df[
                                                                'total percentage of requests where some data produced'] * \
                                                            df['total requests for user data'] / 100.0
        df['number of requests where some data produced'] = df[
            'number of requests where some data produced'].round()
        # this doesn't seem to work: .astype(int, errors='ignore')

        df['preservations_num_affected'] = df[
            'preservations requested']  # Assume 1:1 mapping on requests:accounts

        builder = DataFrameBuilder(df_in=df, df_out=self.df_out, platform='Facebook', platform_property='Facebook',
                                   report_start=report_start, report_end=report_end)

        # Extract requests for user data from governments:
        builder.extract_columns('requests for user data', 'facebook other',
                                'total requests for user data', 'total user accounts referenced',
                                'number of requests where some data produced')

        # Extract content restriction requests:
        builder.extract_columns('content restrictions', 'all', 'content restrictions', 'content_num_affected',
                                'content_num_complied')

        # Extract account preservation requests
        builder.extract_columns('requests for user data', 'preservation requests',
                                'preservations requested', 'preservations_num_affected', 'users / accounts preserved')

        self.df_out = builder.get_df()
        return self.df_out

    def fetch_all(self):
        start_year = 2013
        end_year = datetime.datetime.utcnow().year

        available_urls = self.get_urls(start_year, end_year)

        self.df_out = self.process_urls(available_urls)

        return self.df_out

    def get_urls(self, start_year, end_year):
        source = SemiannualUrlSource({"url_template": "https://transparency.facebook.com/download/$report_year-$facebook_period/", "start_year": start_year, "end_year": end_year})

        return source.get()

    def expected_source_columns_array(self):
        return [
            ["Country","Requests for User Data","User Accounts Referenced","Percentage of requests where some data produced","Content Restrictions"],
            ["Country","Total Requests for User Data","Total User Accounts Referenced","Total Percentage of Requests Where Some Data Produced","Content Restrictions","Preservations Requested","Users/Accounts Preserved"],
            ["Country","Requests for User Data","User Accounts Referenced","Percentage of requests where some data produced"],
        ]

