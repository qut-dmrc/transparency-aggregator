import textwrap
import unittest
from io import StringIO

import numpy as np
import pandas as pd

import utils
from simple_columns_checker import SimpleColumnsChecker


class TestSimpleColumnsChecker(unittest.TestCase):
    def setUp(self):
        self.checker = SimpleColumnsChecker({'expected_source_columns': ['apple', 'banana', 'cherry']})

    def sample_df(self):
        csv = \
            """
            apple,banana,cherry
            1,2,3
            4,5,6
            """
        df = pd.read_csv(StringIO(textwrap.dedent(csv)), encoding="UTF-8", dtype=np.object_)
        return df

    def test_check_should_pass(self):
        df = self.sample_df()
        df_out = self.checker.check(df)
        self.assertTrue(True)  # if it doesn't cause an exception, it passes

    def test_check_extra_column_should_cause_assumption_error(self):
        df = self.sample_df()
        df['extra col'] = 1
        with self.assertRaises(utils.AssumptionError) as context:
            with self.assertLogs(level="ERROR") as logger:
                df_out = self.checker.check(df)

        self.assertIn('Unexpected extra columns: ["extra col"]', str(context.exception))

    def test_check_missing_columns_should_cause_assumption_error(self):
        df = self.sample_df()
        df.drop('banana', 1, inplace=True)
        with self.assertRaises(utils.AssumptionError) as context:
            with self.assertLogs(level="ERROR") as logger:
                df_out = self.checker.check(df)

        self.assertIn('Unexpected missing columns: ["banana"]', str(context.exception))
