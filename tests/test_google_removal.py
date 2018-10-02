import textwrap
from tests.transparency_test_case import TransparencyTestCase
from io import StringIO

import numpy as np
import pandas as pd

import transparency.utils as utils
from transparency.trans_google_removal import TransGoogleRemoval


class TestTransGoogle(TransparencyTestCase):
    # self.google = None

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        self.google = TransGoogleRemoval()

    def tearDown(self):
        pass

    def test_get_urls_should_return_correct_config(self):
        available_urls = self.google.get_urls()

        self.assertEqual(1, len(available_urls))
        self.assertEqual('https://storage.googleapis.com/transparencyreport/google-government-removals.zip',
                         available_urls[0]['url'])
        self.assertEqual('', available_urls[0]['report_start'])
        self.assertEqual('', available_urls[0]['report_end'])

    def test_process_urls_should_load_data(self):
        available_urls = [
            {'url': 'https://storage.googleapis.com/transparencyreport/google-government-removals.zip', 'report_start': '',
             'report_end': ''}]

        df_out = self.google.process_urls(available_urls)
        self.assertEqual('Brazil', df_out['country'][5])
        self.assertEqual(291, df_out['num_requests'][5])

    def sample_df(self):
        csv = \
            """
            Period Ending,Country,CLDR Territory Code,All Requests: Number of Requests,All Requests: % Fully Or Partially Complied With,All Requests: Items Requested To Be Removed,Court Orders: Number of Requests,Court Orders: % Fully Or Partially Complied With,Court Orders: Items Requested To Be Removed,"Other Requests (Executive, Police, etc.): Number of Requests","Other Requests (Executive, Police, etc.): % Fully Or Partially Complied With","Other Requests (Executive, Police, etc.): Items Requested To Be Removed"
            2009-12-31,Argentina,AR,42,88,,41,,,1,,
            2009-12-31,Armenia,AM,<10,0,,,,,,,
            2009-12-31,Australia,AU,17,53,,,,,17,,
            2009-12-31,Austria,AT,<10,60,,,,,,,
            2009-12-31,Belgium,BE,<10,0,,,,,,,
            2009-12-31,Brazil,BR,291,82,,165,,,126,,
            """

        df = pd.read_csv(StringIO(textwrap.dedent(csv)), encoding="UTF-8", dtype=np.object_)
        return df

    def test_process_with_check_should_load_data(self):
        df = self.sample_df()
        df_out = self.google.process_with_check(df, '', '')
        self.assertEqual('Australia', df_out['country'][2])
        self.assertEqual(17, df_out['num_requests'][2])
        self.assertEqual(pd.Timestamp("2009-07-01 00:00:00"), df_out['report_start'][2])
        self.assertEqual(pd.Timestamp("2009-12-31 23:59:59"), df_out['report_end'][2])

    def test_process_with_check_extra_column_should_cause_assumption_error(self):
        df = self.sample_df()
        df['extra col'] = 1
        with self.assertRaises(utils.AssumptionError) as context:
            with self.assertLogs(level="ERROR") as logger:
                df_out = self.google.process_with_check(df, '', '')

        self.assertIn('Unexpected extra columns: ["extra col"]', str(context.exception))

    def test_process_with_check_missing_columns_should_cause_assumption_error(self):
        df = self.sample_df()
        df.drop('Period Ending', 1, inplace=True)
        with self.assertRaises(utils.AssumptionError) as context:
            with self.assertLogs(level="ERROR") as logger:
                df_out = self.google.process_with_check(df, '', '')

        self.assertIn('Unexpected missing columns: ["period ending"]', str(context.exception))
