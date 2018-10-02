""" Fetch and read Facebook transparency data """
import datetime

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.orchestrator import Orchestrator
from transparency.semiannual_url_source import SemiannualUrlSource


class TransFacebook(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        col_map = {
            'requests for user data': 'total requests for user data',
            'user accounts referenced': 'total user accounts referenced',
            'percentage of requests where some data produced': 'total percentage of requests where some data produced',
        }

        df.columns = df.columns.str.lower()
        df.rename(columns=col_map, inplace=True)

        utils.df_strip_char(df, 'total percentage of requests where some data produced', '%')

        # convert strings to numbers
        numeric_cols = ['total requests for user data', 'total user accounts referenced',
                        'total percentage of requests where some data produced', 'content restrictions',
                        'preservations requested',
                        'preservations_num_affected', 'usersaccounts preserved']

        utils.df_convert_to_numeric(df, numeric_cols)

        df['number of requests where some data produced'] = df[
                                                                'total percentage of requests where some data produced'] * \
                                                            df['total requests for user data'] / 100.0
        df['number of requests where some data produced'] = df[
            'number of requests where some data produced'].round()
        # this doesn't seem to work: .astype(int, errors='ignore')

        builder = DataFrameBuilder(df_in=df, platform='Facebook', platform_property='Facebook',
                                   report_start=report_start, report_end=report_end)

        # Extract requests for user data from governments:
        builder.extract_columns(
            request_type='requests for user data',
            request_subtype='all',
            num_requests_col='total requests for user data',
            num_accounts_specified_col='total user accounts referenced',
            num_requests_complied_col='number of requests where some data produced',
            num_accounts_complied_col='',
        )

        # Extract content restriction requests:
        builder.extract_columns(
            request_type='content restrictions',
            request_subtype='all',
            num_requests_col='content restrictions',
            num_accounts_specified_col='',
            num_requests_complied_col=''
        )

        # Extract account preservation requests
        builder.extract_columns(
            request_type='preservation requests',
            request_subtype='all',
            num_requests_col='preservations requested',
            num_accounts_specified_col='usersaccounts preserved',
            num_requests_complied_col='',  # TODO: check with facebook if all preservation requests are actioned
            num_accounts_complied_col='',
        )

        df_out = builder.get_df()
        return df_out

    def fetch_all(self):
        start_year = 2013
        end_year = datetime.datetime.utcnow().year

        available_urls = self.get_urls(start_year, end_year)

        df_out = self.process_urls(available_urls)

        return df_out

    def get_urls(self, start_year, end_year):
        source = SemiannualUrlSource(
            {"url_template": "https://transparency.facebook.com/download/$report_year-$facebook_period/",
             "start_year": start_year, "end_year": end_year})

        return source.get()

    def expected_source_columns_array(self):
        return [
            ["Country", "Requests for User Data", "User Accounts Referenced",
             "Percentage of requests where some data produced", "Content Restrictions"],
            ["Country", "Total Requests for User Data", "Total User Accounts Referenced",
             "Total Percentage of Requests Where Some Data Produced", "Content Restrictions", "Preservations Requested",
             "Users/Accounts Preserved"],
            ["Country", "Requests for User Data", "User Accounts Referenced",
             "Percentage of requests where some data produced"],
        ]
