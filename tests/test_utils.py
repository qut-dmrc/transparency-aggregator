import numbers
import unittest
import unittest.mock as mock

import pandas as pd

import transparency.utils as utils
from tests.transparency_test_case import TransparencyTestCase


class TestUtils(TransparencyTestCase):

    def test_str_to_date_with_format_parses_date(self):
        got = utils.str_to_date('01/02/2000', "%d/%m/%Y")
        self.assertEqual(1, got.day)
        self.assertEqual(2, got.month)
        self.assertEqual(2000, got.year)

    def test_str_to_date_without_format_parses_date(self):
        got = utils.str_to_date('2000-02-01')
        self.assertEqual(1, got.day)
        self.assertEqual(2, got.month)
        self.assertEqual(2000, got.year)

    def test_setup_logging(self):
        pass  # TODO

    def test_df_fix_columns(self):
        d = {
            'NUMBER requests': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
            'number affected': pd.Series([4, 5, 6], index=['a', 'b', 'c']),
        }
        df = pd.DataFrame(d)
        utils.df_fix_columns(df)
        self.assertEqual(['number requests', 'number affected'], df.columns.tolist())

    def test_df_strip_char(self):
        d = {
            'a': pd.Series(['1', '2%', '3'], index=['a', 'b', 'c']),
        }
        df = pd.DataFrame(d)
        utils.df_strip_char(df, 'a', '%')

        self.assertEqual(['1', '2', '3'], df['a'].as_matrix().tolist())

    def test_df_convert_to_numeric(self):
        d = {
            'a': pd.Series(['11', '2', '3'], index=['a', 'b', 'c']),
            'b': pd.Series(['4', '5', '6'], index=['a', 'b', 'c']),
        }
        df = pd.DataFrame(d)
        utils.df_convert_to_numeric(df, ['a', 'b'])

        self.assertTrue(isinstance(df['a'][0], numbers.Number))

    def test_check_assumption(self):
        with mock.patch('transparency.utils.logging.error') as mock_ret:
            utils.check_assumption(True, "Value should be true")
            mock_ret.assert_not_called()

    def test_check_assumption_failed(self):
        with self.assertRaises(utils.AssumptionError) as context:
            with self.assertLogs(level="ERROR") as logger:
                utils.check_assumption(False, "Value should be true")

                self.assertEqual(1, len(logger.output))
                self.assertIn('ERROR:root:Assumption failed: Value should be true', logger.output[0])
        self.assertTrue('Value should be true' in str(context.exception))

    def test_df_convert_to_lower(self):
        d = {
            'a': pd.Series(['Test']),
            'b': pd.Series(['TEST']),
            'c': pd.Series(['Test']),
        }
        df = pd.DataFrame(d)
        utils.df_convert_to_lower(df, ['a', 'b'])

        self.assertEqual('test', df['a'][0])
        self.assertEqual('test', df['b'][0])
        self.assertEqual('Test', df['c'][0])

    def test_df_convert_to_int(self):
        d = {
            'a': pd.Series([1, '2', 3.1, None, float('nan')], index=[1,2,3,4,5])
        }
        df = pd.DataFrame(d)

        utils.df_convert_to_int(df, ['a'])

        self.assertEqualAndInt(1, df['a'][1])
        self.assertEqualAndInt(2, df['a'][2])
        self.assertEqualAndInt(3, df['a'][3])
        self.assertIsNone(df['a'][4])
        self.assertIsNone(df['a'][5])


    def test_df_convert_from_percentage(self):
        pass
# df, pc_col, total_col, dest_col):
# df[dest_col] = df[total_col] * df[pc_col] / 100.0
# df[dest_col] = df[dest_col].round()
