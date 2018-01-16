import unittest
from io import StringIO

import numpy as np
import pandas as pd

from desired_columns_mutator import DesiredColumnsMutator


class TestDesiredColumnsMutator(unittest.TestCase):
    def setUp(self):
        x = {'desired_columns': ['apple', 'banana', 'cherry']}
        self.mutator = DesiredColumnsMutator(x)

    def sample_df(self):
        csv = \
            """
            apple,banana,cherry
            1,2,3
            4,5,6
            """
        df = pd.read_csv(StringIO(csv), encoding="UTF-8", dtype=np.object_)
        return df

    def test_mutate_should_add_missing_columns(self):
        df = self.sample_df()
        df.drop('banana', 1, inplace=True)
        df_out = self.mutator.mutate(df)
        self.assertEqual(['apple', 'banana', 'cherry'], list(df_out.columns.values))

    def test_mutate_should_remove_extra_columns(self):
        df = self.sample_df()
        df['extra col'] = 1
        df_out = self.mutator.mutate(df)
        self.assertEqual(['apple', 'banana', 'cherry'], list(df_out.columns.values))
