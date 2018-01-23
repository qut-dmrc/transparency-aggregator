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
        self.assertEqual("849.0", row['num_accounts_specified'])
        self.assertEqual("542.0", row['num_requests_complied'])

    def test_facebook_2013(self):
        row = self.indexed_df.loc[
            "2013-01-01 00:00:00", "Facebook", "Facebook", "United States", "requests for user data", "facebook other"]

        self.assertEqual("2013-06-30 23:59:59", row['report_end'])
        self.assertEqual("11000", row['num_requests'])
        self.assertEqual("20000.0", row['num_accounts_specified'])
        self.assertEqual("8690.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_twitter_2012(self):
        row = self.indexed_df.loc[
            "2012-01-01 00:00:00", "Twitter", "Twitter", "Canada", "requests for user data", "all"]

        self.assertEqual("2012-06-30 23:59:59", row['report_end'])
        self.assertEqual("11.0", row['num_requests'])
        self.assertEqual("12.0", row['num_accounts_specified'])
        self.assertEqual("2.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_twitter_2017(self):
        row = self.indexed_df.loc[
            "2017-01-01 00:00:00", "Twitter", "Twitter", "Australia", "requests for user data", "all"]

        self.assertEqual("2017-06-30 23:59:59", row['report_end'])
        self.assertEqual("14.0", row['num_requests'])
        self.assertEqual("20.0", row['num_accounts_specified'])
        self.assertEqual("6.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2009(self):
        # the error:
        #   KeyError: 'the label [Google] is not in the [columns]'
        # just means the row wasn't found.  Note that it is case sensitive.
        row = self.indexed_df.loc[
            "2009-07-01 00:00:00", "Google", "Google", "Australia", "requests for user data", "all"]

        self.assertEqual("2009-12-31 23:59:59", row['report_end'])
        self.assertEqual("155", row['num_requests'])
        self.assertTrue(math.isnan(row['num_accounts_specified']))
        self.assertTrue(math.isnan(row['num_requests_complied']))
        self.assertTrue(math.isnan(row['num_accounts_complied']))    
    

    def test_google_2010(self):
        row = self.indexed_df.loc[
            "2010-07-01 00:00:00", "Google", "Google", "Belgium", "requests for user data", "all"]

        self.assertEqual("2010-12-31 23:59:59", row['report_end'])
        self.assertEqual("85", row['num_requests'])
        self.assertTrue(math.isnan(row['num_accounts_specified']))
        self.assertEqual("62.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2012(self):
        row = self.indexed_df.loc[
            "2012-07-01 00:00:00", "Google", "Google", "United States", "requests for user data", "legal requests"]

        self.assertEqual("2012-12-31 23:59:59", row['report_end'])
        self.assertEqual("758", row['num_requests'])
        self.assertEqual("1249.0", row['num_accounts_specified'])
        self.assertEqual("682.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2013(self):
        row = self.indexed_df.loc[
            "2013-07-01 00:00:00", "Google", "Google", "United States", "requests for user data", "pen register orders"]

        self.assertEqual("2013-12-31 23:59:59", row['report_end'])
        self.assertEqual("140", row['num_requests'])
        self.assertEqual("259.0", row['num_accounts_specified'])
        self.assertEqual("126.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2014_preservation_requests(self):
        row = self.indexed_df.loc[
            "2014-07-01 00:00:00", "Google", "Google", "Canada", "preservation requests", "preservation requests"]

        self.assertEqual("2014-12-31 23:59:59", row['report_end'])
        self.assertEqual("26", row['num_requests'])
        self.assertEqual("50.0", row['num_accounts_specified'])
        self.assertTrue(math.isnan(row['num_requests_complied']))
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2014_legal_requests(self):
        row = self.indexed_df.loc[
            "2014-07-01 00:00:00", "Google", "Google", "Canada", "requests for user data", "legal requests"]

        self.assertEqual("2014-12-31 23:59:59", row['report_end'])
        self.assertEqual("26", row['num_requests'])
        self.assertEqual("27.0", row['num_accounts_specified'])
        self.assertEqual("6.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_linkedin_2012(self):
        row = self.indexed_df.loc[
            "2012-07-01 00:00:00", "LinkedIn", "LinkedIn", "United States", "requests for user data", "all"]

        self.assertEqual("2012-12-31 23:59:59", row['report_end'])
        self.assertEqual("45", row['num_requests'])
        self.assertTrue(math.isnan(row['num_accounts_specified']))
        self.assertEqual("36.0", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied'])) 

    def test_linkedin_2017(self):
        row = self.indexed_df.loc[
            "2017-01-01 00:00:00", "LinkedIn", "LinkedIn", "United States", "requests for user data", "all"]

        self.assertEqual("2017-06-30 23:59:59", row['report_end'])
        self.assertEqual("187", row['num_requests'])
        self.assertEqual("594.0", row['num_accounts_specified'])
        self.assertEqual("133.0", row['num_requests_complied'])
        self.assertEqual("229.0", row['num_accounts_complied'])       

# "report_start","report_end","platform","property","country","request_type","request_subtype","num_requests","num_accounts_specified","num_requests_complied","num_accounts_complied","agency","reason"


if __name__ == '__main__':
    unittest.main()
