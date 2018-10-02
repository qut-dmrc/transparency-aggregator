import os
from tests.transparency_test_case import TransparencyTestCase

from transparency import utils
from transparency.snap_reader import SnapReader
from datetime import datetime

class TestSnapReader(TransparencyTestCase):
    def setUp(self):
        self.reader = SnapReader({})

    def test_read_correctly_handles_numbers(self):
        df = self.reader.read(os.path.join(os.path.dirname(__file__), 'files/snap_sample.html'))

        self.assertEqual('Australia', df['country'][0])  # ensure numbers are loaded as strings
        self.assertEqual(datetime(2015, 7, 1), df['report start from table'][0])
        self.assertEqual(datetime(2015, 12, 31, 23, 59, 59), df['report end from table'][0])
        self.assertEqual('50%', df['Percentage of Emergency Requests where some data was produced'][0])
        self.assertEqual(5, df['Account Identifiers* for Other Information Requests'][0])
        self.assertNaN(df['Account Identifiers* for Other Information Requests'][1])

