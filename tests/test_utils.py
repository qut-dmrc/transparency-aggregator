import logging
from logging.handlers import RotatingFileHandler
from dateutil.parser import parse
from datetime import datetime, date
import numpy as np
import pandas as pd
import numbers

import utils

import unittest

class TestUtils(unittest.TestCase):

	def test_str_to_date(self):
		pass #TODO

	def test_setup_logging(self):
		pass #TODO


	def test_df_fix_columns(self):
		d = {
			'NUMBER requests' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
			'number affected' : pd.Series([4, 5, 6], index=['a', 'b', 'c']),
		}
		df = pd.DataFrame(d)
		utils.df_fix_columns(df)
		self.assertEqual(['number requests', 'number affected'], df.columns.tolist())

	def test_df_strip_char(self):
		d = {
			'a' : pd.Series(['1', '2%', '3'], index=['a', 'b', 'c']),
		}
		df = pd.DataFrame(d)
		utils.df_strip_char(df, 'a', '%')
		
		self.assertEqual(['1', '2', '3'], df['a'].as_matrix().tolist())

	def df_convert_to_numeric(self):
		d = {
			'a' : pd.Series(['11', '2', '3'], index=['a', 'b', 'c']),
			'b' : pd.Series([4, 5, 6], index=['a', 'b', 'c']),
		}
		df = pd.DataFrame(d)
		utils.df_convert_to_numeric(df, ['a', 'b'])
		
		self.assertTrue(isinstance(df['a'][0], numbers.Number))
		





	def test_df_convert_from_percentage(self):
		pass
		#df, pc_col, total_col, dest_col):
		#df[dest_col] = df[total_col] * df[pc_col] / 100.0
		#df[dest_col] = df[dest_col].round()
