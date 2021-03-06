import logging
import math
import os
import subprocess
import unittest

import numpy as np
import pandas as pd

from tests.transparency_test_case import TransparencyTestCase


class TestMain(TransparencyTestCase):
    """
    This test compares the output of the system with a few datapoints
    collected by hand by looking at transparency websites
    """
    @classmethod
    def setUpClass(cls):
        use_old = os.environ.get('SYSTEM_TEST_USE_OLD_OUTPUT')
        os.chdir(os.path.join(os.path.dirname(__file__), '..'))  # change working directory to root of project
        output_file = 'system_tests/output/output.csv'
        if not use_old:
            output = subprocess.check_output(
                ['python', 'main.py', '--csv-output', output_file, '--get-all'])

            if output:
                print(output)
        else:
            logging.warning(
                'SYSTEM_TEST_USE_OLD_OUTPUT is set\n\n*********************\n*********************\n\n  USING OLD OUTPUT!\n\n*********************\n*********************\n')

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

    def test_facebook_2017_user_data_request(self):
        row = self.indexed_df.loc[
            "2017-01-01 00:00:00", "Facebook", "Facebook", "Australia", "requests for user data", "all"]

        self.assertEqual("2017-06-30 23:59:59", row['report_end'])
        self.assertEqual("704", row['num_requests'])
        self.assertEqual("849", row['num_accounts_specified'])
        self.assertEqual("542", row['num_requests_complied'])

    def test_facebook_2017_preservation_request(self):
        row = self.indexed_df.loc[
            "2017-01-01 00:00:00", "Facebook", "Facebook", "Canada", "preservation requests", "all"]

        self.assertEqual("2017-06-30 23:59:59", row['report_end'])
        self.assertEqual("1452", row['num_requests'])
        self.assertEqual("2378", row['num_accounts_specified'])
        self.assertNaN(row['num_requests_complied'])

    def test_facebook_2013_user_data_request(self):
        row = self.indexed_df.loc[
            "2013-01-01 00:00:00", "Facebook", "Facebook", "United States", "requests for user data", "all"]

        self.assertEqual("2013-06-30 23:59:59", row['report_end'])
        self.assertEqual("11000", row['num_requests'])
        self.assertEqual("20000", row['num_accounts_specified'])
        self.assertEqual("8690", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_twitter_2012_user_data_request(self):
        row = self.indexed_df.loc[
            "2012-01-01 00:00:00", "Twitter", "Twitter", "Canada", "requests for user data", "all"]

        self.assertEqual("2012-06-30 23:59:59", row['report_end'])
        self.assertEqual("11", row['num_requests'])
        self.assertEqual("12", row['num_accounts_specified'])
        self.assertEqual("2", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_twitter_2017_user_data_request(self):
        row = self.indexed_df.loc[
            "2017-01-01 00:00:00", "Twitter", "Twitter", "Australia", "requests for user data", "all"]

        self.assertEqual("2017-06-30 23:59:59", row['report_end'])
        self.assertEqual("14", row['num_requests'])
        self.assertEqual("20", row['num_accounts_specified'])
        self.assertEqual("6", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2009_user_data_request(self):
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

    def test_google_2010_user_data_request(self):
        row = self.indexed_df.loc[
            "2010-07-01 00:00:00", "Google", "Google", "Belgium", "requests for user data", "all"]

        self.assertEqual("2010-12-31 23:59:59", row['report_end'])
        self.assertEqual("85", row['num_requests'])
        self.assertTrue(math.isnan(row['num_accounts_specified']))
        self.assertEqual("62", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2012_legal_request(self):
        row = self.indexed_df.loc[
            "2012-07-01 00:00:00", "Google", "Google", "United States", "requests for user data", "legal requests"]

        self.assertEqual("2012-12-31 23:59:59", row['report_end'])
        self.assertEqual("758", row['num_requests'])
        self.assertEqual("1249", row['num_accounts_specified'])
        self.assertEqual("682", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2013_pen_register_orders(self):
        row = self.indexed_df.loc[
            "2013-07-01 00:00:00", "Google", "Google", "United States", "requests for user data", "pen register orders"]

        self.assertEqual("2013-12-31 23:59:59", row['report_end'])
        self.assertEqual("140", row['num_requests'])
        self.assertEqual("259", row['num_accounts_specified'])
        self.assertEqual("126", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2014_preservation_requests(self):
        row = self.indexed_df.loc[
            "2014-07-01 00:00:00", "Google", "Google", "Canada", "preservation requests", "all"]

        self.assertEqual("2014-12-31 23:59:59", row['report_end'])
        self.assertEqual("26", row['num_requests'])
        self.assertEqual("50", row['num_accounts_specified'])
        self.assertTrue(math.isnan(row['num_requests_complied']))
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_google_2014_legal_requests(self):
        row = self.indexed_df.loc[
            "2014-07-01 00:00:00", "Google", "Google", "Canada", "requests for user data", "legal requests"]

        self.assertEqual("2014-12-31 23:59:59", row['report_end'])
        self.assertEqual("26", row['num_requests'])
        self.assertEqual("27", row['num_accounts_specified'])
        self.assertEqual("6", row['num_requests_complied'])
        self.assertTrue(math.isnan(row['num_accounts_complied']))

    def test_linkedin_2012_user_data_request(self):
        row = self.indexed_df.loc[
            "2012-07-01 00:00:00", "LinkedIn", "LinkedIn", "United States", "requests for user data", "all"]

        self.assertEqual("2012-12-31 23:59:59", row['report_end'])
        self.assertEqual("45", row['num_requests'])
        self.assertEqual("49", row['num_accounts_specified'])
        self.assertEqual("36", row['num_requests_complied'])
        self.assertNaN(row['num_accounts_complied'])

    def test_linkedin_2017_user_data_request(self):
        row = self.indexed_df.loc[
            "2017-01-01 00:00:00", "LinkedIn", "LinkedIn", "United States", "requests for user data", "all"]

        self.assertEqual("2017-06-30 23:59:59", row['report_end'])
        self.assertEqual("187", row['num_requests'])
        self.assertEqual("594", row['num_accounts_specified'])
        self.assertEqual("133", row['num_requests_complied'])
        self.assertEqual("229", row['num_accounts_complied'])

    def test_snapchat_2016_user_data_request_emergency(self):
        row = self.indexed_df.loc[
            "2016-01-01 00:00:00", "Snap", "Snapchat", "Canada", "requests for user data", "emergency disclosure requests"
        ]

        self.assertEqual("2016-06-30 23:59:59", row['report_end'])
        self.assertEqual("13", row['num_requests'])
        self.assertEqual("17", row['num_accounts_specified'])
        self.assertEqual("10", row['num_requests_complied'])


    def test_snapchat_2016_user_data_request_other(self):
        row = self.indexed_df.loc[
            "2015-01-01 00:00:00", "Snap", "Snapchat", "France", "requests for user data", "non emergency disclosure requests"
        ]

        self.assertEqual("2015-06-30 23:59:59", row['report_end'])
        self.assertEqual("37", row['num_requests'])
        self.assertEqual("50", row['num_accounts_specified'])
        self.assertEqual("0", row['num_requests_complied'])


# "report_start","report_end","platform","property","country","request_type","request_subtype","num_requests","num_accounts_specified","num_requests_complied","num_accounts_complied","agency","reason"


if __name__ == '__main__':
    unittest.main()
