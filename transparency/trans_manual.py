"""
Read and aggregate manually entered CSVs from the directory ./manual
"""
import logging

from transparency import utils
from transparency.directory_source import DirectorySource
from transparency.orchestrator import Orchestrator


class TransManual(Orchestrator):

    def process(self, df, report_start, report_end):
        self.df_out = df
        return self.df_out

    def fetch_all(self):
        available_urls = self.get_urls()

        self.df_out = self.process_urls(available_urls)

        return self.df_out

    def expected_source_columns_array(self):
        return [["report_start", "report_end", "platform", "property", "country", "request_type", "request_subtype",
                 "num_requests", "num_accounts_specified", "num_requests_complied", "num_accounts_complied", "agency",
                 "reason"]]

    def get_urls(self):
        source = DirectorySource({'directory': utils.make_path("manual")})

        return source.get()

    def process_urls(self, available_urls):
        for data in available_urls:
            url = data['url']

            logging.info("Processing manual transparency report from {}".format(url))

            df = self.read(url)
            self.process_with_check(df, report_start=None, report_end=None)

        return self.coerce_df(self.df_out)
