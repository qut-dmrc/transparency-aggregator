from tests.transparency_test_case import TransparencyTestCase

import os

from transparency.csv_reader import CSVReader


class TestCSVReader(TransparencyTestCase):
    def setUp(self):
        self.reader = CSVReader({})

    def test_read_correctly_handles_numbers(self):
        df = self.reader.read(os.path.join(os.path.dirname(__file__), 'files/simple_csv_file.csv'))
        self.assertEqual('1', df['a'][0])  # ensure numbers are loaded as strings
        self.assertEqual('d', df['b'][0])
