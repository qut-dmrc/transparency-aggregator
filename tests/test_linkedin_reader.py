import unittest

import os

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

        self.assertEqual('India', df['country'][2])
        self.assertEqual('31', df['accountsImpacted'][2])
        self.assertEqual('32%', df['percentProvided'][2])
        self.assertEqual('33', df['memberDataRequests'][2])
        self.assertEqual('34', df['subjectToRequest'][2])