import textwrap
import unittest
from io import StringIO

import numpy as np
import pandas as pd

import utils
from trans_google import TransGoogle


class TestTransGoogle(unittest.TestCase):
    # self.google = None

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        self.google = TransGoogle()

    def tearDown(self):
        pass

    def test_get_urls_should_return_correct_config(self):
        available_urls = self.google.get_urls()

        self.assertEqual(1, len(available_urls))
        self.assertEqual('https://storage.googleapis.com/transparencyreport/google-user-data-requests.zip',
                         available_urls[0]['url'])
        self.assertEqual('', available_urls[0]['start_date'])
        self.assertEqual('', available_urls[0]['end_date'])

    def test_process_urls_should_load_data(self):
        available_urls = [
            {'url': 'https://storage.googleapis.com/transparencyreport/google-user-data-requests.zip', 'start_date': '',
             'end_date': ''}]

        df_out = self.google.process_urls(available_urls)
        self.assertEqual('Brazil', df_out['country'][3])
        self.assertEqual(3663, df_out['num_requests'][3])

    # TODO Test from fixed data

    def sample_df(self):
        csv = \
            """
            Period Ending,Country,CLDR Territory Code,Legal Process,User Data Requests,Percentage of requests where some data produced,Users/Accounts Specified
            31/12/09,Argentina,AR,All,98,,
            31/12/09,Australia,AU,All,155,,
            31/12/09,Belgium,BE,All,67,,
            """

        df = pd.read_csv(StringIO(textwrap.dedent(csv)), encoding="UTF-8", dtype=np.object_)
        return df

    def test_process_with_check_should_load_data(self):
        df = self.sample_df()
        df_out = self.google.process_with_check(df, '', '')
        self.assertEqual('Australia', df_out['country'][1])
        self.assertEqual(155, df_out['num_requests'][1])

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

        self.assertIn('Unexpected missing columns: ["Period Ending"]', str(context.exception))


# self.process(df, start_date=start_date, end_date=end_date)
if __name__ == '__main__':
    unittest.main()
