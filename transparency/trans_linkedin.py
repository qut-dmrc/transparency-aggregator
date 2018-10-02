""" Fetch and read Linkedin transparency data """

import transparency.utils as utils
from transparency.data_frame_builder import DataFrameBuilder
from transparency.linkedin_reader import LinkedinReader
from transparency.orchestrator import Orchestrator
from transparency.static_source import StaticSource


class TransLinkedin(Orchestrator):

    def process(self, df, report_start, report_end):
        utils.df_fix_columns(df)

        utils.df_strip_char(df, 'percentprovided', '%')

        numeric_cols = ['accountsimpacted', 'memberdatarequests', 'percentprovided', 'subjecttorequest']

        utils.df_convert_to_numeric(df, numeric_cols)

        builder = DataFrameBuilder(df_in=df, platform='LinkedIn', platform_property='LinkedIn',
                                   report_start='', report_end='')

        utils.df_convert_from_percentage(df, 'percentprovided', 'memberdatarequests',
                                         'number where some information produced')

        # Extract requests for user data from governments:
        builder.extract_columns(
            request_type='requests for user data',
            request_subtype='all',
            num_requests_col='memberdatarequests',
            num_accounts_specified_col='subjecttorequest',
            num_requests_complied_col='number where some information produced',
            num_accounts_complied_col='accountsimpacted',
        )

        df_out = builder.get_df()

        df_out['reportend'] = df['reportend']
        df_out['reportstart'] = df['reportstart']

        return df_out

    def fetch_all(self):
        available_urls = self.get_urls()

        df_out = self.process_urls(available_urls)

        return df_out

    def expected_source_columns_array(self):
        return [["country", "percentProvided", "subjectToRequest", "report_start", "report_end", "accountsImpacted",
                 "memberDataRequests", "isMLAT"]]

    def get_urls(self):
        source = StaticSource({'data': [{
            "url": "https://www.linkedin.com/legal/transparency",
            "report_start": '',
            "report_end": '',
        }]})

        return source.get()

    def read(self, filename):
        reader = LinkedinReader({})
        return reader.read(filename)
