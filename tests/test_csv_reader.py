from csv_reader import CSVReader
import unittest
import logging

class TestCSVReader(unittest.TestCase):
	def setUp(self):
		self.reader = CSVReader()

	def test_read_correctly_handles_numbers(self):
		df = self.reader.read('tests/source/simple_csv_file')
		self.assertEqual('1', df['a'][0])  # ensure numbers are loaded as strings
		self.assertEqual('d', df['b'][0])
