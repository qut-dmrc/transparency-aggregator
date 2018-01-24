"""
Read and aggregate manually entered CSVs from the directory ./manual
"""
import logging

import pandas as pd

from transparency import utils
from transparency.directory_source import DirectorySource
from transparency.orchestrator import Orchestrator


class TransManual(Orchestrator):

    def process(self, df, report_start, report_end):
        return df

    def fetch_all(self):
        available_urls = self.get_urls()

        df_out = self.process_urls(available_urls)

        return df_out

    def expected_source_columns_array(self):
        return [["report_start", "report_end", "platform", "property", "country", "request_type", "request_subtype",
                 "num_requests", "num_accounts_specified", "num_requests_complied", "num_accounts_complied", "agency",
                 "reason"]]

    def get_urls(self):
        source = DirectorySource({'directory': utils.make_path("manual")})

        return source.get()

    def process_urls(self, available_urls):
        df_out = pd.DataFrame()
        for data in available_urls:
            url = data['url']

            logging.info("Processing manual transparency report from {}".format(url))

            src_df = self.read(url)
            dst_df = self.process_with_check(src_df, report_start=None, report_end=None)
            df_out = df_out.append(dst_df)

        return self.coerce_df(df_out)
