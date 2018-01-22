import subprocess
import unittest
import math

import numpy as np
import pandas as pd


class TestMain(unittest.TestCase):

    def setUp(self):
        output = subprocess.check_output(
            ['python', 'main.py', '--csv-output', 'system_tests/output/output.csv', '--get-all'])

        if output:
            print(output)

        self.df = pd.read_csv('system_tests/output/output.csv', encoding="UTF-8", dtype=np.object_)

        self.indexed_df = self.df.set_index([
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
