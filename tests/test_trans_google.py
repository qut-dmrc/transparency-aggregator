from trans_google import TransGoogle
import unittest
import logging

class TestTransGoogle(unittest.TestCase):
		# self.google = None

	@classmethod
	def setup_class(cls):
		"""This method is run once for each class before any tests are run"""
		pass

	def setUp(self):
		self.google = TransGoogle()

	def tearDown(self):
		pass

	def test_get_urls(self):
		available_urls = self.google.get_urls()

		self.assertEqual(1, len(available_urls))
		self.assertEqual('https://storage.googleapis.com/transparencyreport/google-user-data-requests.zip', available_urls[0]['url'])
		self.assertEqual('', available_urls[0]['start_date'])
		self.assertEqual('', available_urls[0]['end_date'])

	def test_process_urls(self):
		available_urls = [ { 'url': 'https://storage.googleapis.com/transparencyreport/google-user-data-requests.zip', 'start_date': '', 'end_date': ''} ]
		
		df_out = self.google.process_urls(available_urls)
		self.assertEqual('Brazil', df_out['country'][3])
		self.assertEqual(3663, df_out['num_requests'][3])
		#TODO Test from fixed data

if __name__ == '__main__':
	unittest.main()
