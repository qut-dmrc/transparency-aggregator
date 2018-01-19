import os
import unittest

from transparency import utils
from transparency.linkedin_reader import LinkedinReader


class TestLinkedinReader(unittest.TestCase):
    def setUp(self):
        self.reader = LinkedinReader({})

    def test_read_correctly_handles_numbers(self):
        df = self.reader.read(os.path.join(os.path.dirname(__file__), 'files/linkedin_sample.html'))

        self.assertEqual('India', df['country'][0])  # ensure numbers are loaded as strings
        self.assertEqual('2011-07-01 00:00:00', df['report_start'][0])
        self.assertEqual('2011-12-31 23:59:59', df['report_end'][0])

        self.assertEqual('United States', df['country'][1])
        self.assertEqual('2011-07-01 00:00:00', df['report_start'][1])
        self.assertEqual('2011-12-31 23:59:59', df['report_end'][1])

        self.assertEqual('India', df['country'][2])
        self.assertEqual('2012-01-01 00:00:00', df['report_start'][2])
        self.assertEqual('2012-06-30 23:59:59', df['report_end'][2])
        self.assertEqual('31', df['accountsImpacted'][2])
        self.assertEqual('32%', df['percentProvided'][2])
        self.assertEqual('33', df['memberDataRequests'][2])
        self.assertEqual('34', df['subjectToRequest'][2])

    def test_read_correctly_throws_error_when_no_dates_checked(self):
        with self.assertRaises(utils.AssumptionError) as context:
            with self.assertLogs(level="ERROR"):
                self.reader.read(os.path.join(os.path.dirname(__file__), 'files/linkedin_sample_no_date_range.html'))

        expected_message = "No date checks performed. Find another way of checking date assumptions."
        self.assertIn(expected_message, str(context.exception))

    def test_check_date_range_throws_error_when_dates_do_not_match(self):
        with self.assertRaises(utils.AssumptionError) as context:
            with self.assertLogs(level="ERROR"):
                date_range = '2016 July-December - This data point is not used; used for readability.'
                report_start = '2012-01-01 00:00:00'
                report_end = '2012-06-30 23:59:59'

                self.reader.check_date_range(date_range, report_start, report_end)

        expected_message = "Expected '2012 January-June' to be in '2016 July-December - This data point is not used; used for readability.'."
        self.assertIn(expected_message, str(context.exception))

    def test_check_date_range_throws_no_error_when_dates_match(self):
        date_range = '2012 January-June - This data point is not used; used for readability.'
        report_start = '2012-01-01 00:00:00'
        report_end = '2012-06-30 23:59:59'

        self.reader.check_date_range(date_range, report_start, report_end)
        self.assertTrue(True)
