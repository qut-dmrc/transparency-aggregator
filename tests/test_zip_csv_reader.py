import unittest

import os

from transparency.zip_csv_reader import ZipCSVReader


class TestZipCSVReader(unittest.TestCase):
    def setUp(self):
        self.reader = ZipCSVReader({'internal_filename': 'simple_csv_file.csv'})

    def test_read_correctly_handles_numbers(self):
        df = self.reader.read(os.path.join(os.path.dirname(__file__), 'files/simple_zip_csv_file.zip'))
        self.assertEqual('1', df['a'][0])  # ensure numbers are loaded as strings
        self.assertEqual('d', df['b'][0])
