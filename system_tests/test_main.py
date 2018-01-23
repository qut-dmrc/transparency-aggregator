import logging
import math
import subprocess
import unittest
import os

import numpy as np
import pandas as pd


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        use_old = os.environ.get('SYSTEM_TEST_USE_OLD_OUTPUT')
        output_file = 'system_tests/output/output.csv'
        if not use_old:
            output = subprocess.check_output(
                ['python', 'main.py', '--csv-output', output_file, '--get-all'])

            if output:
                print(output)
        else:
            logging.warning('SYSTEM_TEST_USE_OLD_OUTPUT is set\n\n*********************\n*********************\n\n  USING OLD OUTPUT!\n\n*********************\n*********************\n')

        cls._df = pd.read_csv(output_file, encoding="UTF-8", dtype=np.object_)

    def setUp(self):
        self.indexed_df = TestMain._df.set_index([
            'report_start',
            'platform',
            'property',
            'country',
            'request_type',
            'request_subtype',
        ])

    def tearDown(self):
        pass

    def test_facebook_2017(self):
        row = self.indexed_df.loc[
            "2017-01-01 00:00:00", "Facebook", "Facebook", "Australia", "requests for user data", "facebook other"]

        self.assertEqual("2017-06-30 23:59:59", row['report_end'])
        self.assertEqual("704", row['num_requests'])
        self.assertEqual("849", row['num_accounts_specified'])
        self.assertEqual("542.0", row['num_requests_complied'])

    def test_facebook_2013(self):
        row = self.indexed_df.loc[
            "2013-01-01 00:00:00", "Facebook", "Facebook", "United States", "requests for user data", "facebook other"]

        self.assertEqual("2013-06-30 23:59:59", row['report_end'])
        self.assertEqual("11000", row['num_requests'])
        self.assertEqual("20000.0", row['num_accounts_specified'])
        self.assertEqual("8690.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))


# "report_start","report_end","platform","property","country","request_type","request_subtype","num_requests","num_accounts_specified","num_requests_complied","num_accounts_complied","agency","reason"


if __name__ == '__main__':
    unittest.main()
