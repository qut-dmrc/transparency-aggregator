import unittest
from data_frame_builder import DataFrameBuilder
import pandas as pd
from transparency_aggregator import TransparencyAggregator

class TestDataFrameBuilder(unittest.TestCase):

	@classmethod
	def setup_class(cls):
		"""This method is run once for each class before any tests are run"""
		pass	

	def setUp(self): 
		pass

	def sample_df(self):
		d = {
			'number requests' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
			'number affected' : pd.Series([4, 5, 6], index=['a', 'b', 'c']),
			'number complied' : pd.Series([7, 8, 9], index=['a', 'b', 'c']),
			'another number requests' : pd.Series([11, 12, 13], index=['a', 'b', 'c']),
			'another number affected' : pd.Series([14, 15, 16], index=['a', 'b', 'c']),
			'another number complied' : pd.Series([17, 18, 19], index=['a', 'b', 'c']),
			'country' : pd.Series(['aust', 'nz', 'us'], index=['a', 'b', 'c']),
		}
		df = pd.DataFrame(d)	
		return df

	def tearDown(self):
		pass	

	def test_data_frame_builder(self):
		df_in = self.sample_df()
		df_out = pd.DataFrame()
		TransparencyAggregator.coerce_df(df_out)

		cut = DataFrameBuilder(df_in, df_out, 'platform', 'platform_property', '2001-01-01', '2001-06-30')
		cut.extract_columns('request_type', num_requests_col = 'number requests', num_affected_col = 'number affected', num_complied_col = 'number complied')
		cut.extract_columns('another request_type', num_requests_col = 'another number requests', num_affected_col = 'another number affected', num_complied_col = 'another number complied')
		new_df_out = cut.get_df()

		self.assertEqual(6, len(new_df_out.index))
		self.assertEqual('aust', new_df_out['country'][0])
		self.assertEqual('request_type', new_df_out['request_type'][0])
		self.assertEqual(1, new_df_out['num_requests'][0])
		self.assertEqual(4, new_df_out['num_affected'][0])
		self.assertEqual(7, new_df_out['num_complied'][0])

		self.assertEqual('aust', new_df_out['country'][3])
		self.assertEqual('another request_type', new_df_out['request_type'][3])
		self.assertEqual(11, new_df_out['num_requests'][3])
		self.assertEqual(14, new_df_out['num_affected'][3])
		self.assertEqual(17, new_df_out['num_complied'][3])

			

if __name__ == '__main__':
	unittest.main()