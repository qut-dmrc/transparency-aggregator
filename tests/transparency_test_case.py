import textwrap
import unittest
import math

from io import StringIO

import numpy as np
import pandas as pd
import numbers


class TransparencyTestCase(unittest.TestCase):
    def get_df(self, csv):
        """
        Convert a csv string to a dataframe, ignoring whitespace from indents
        """
        df = pd.read_csv(StringIO(textwrap.dedent(csv)), encoding="UTF-8", dtype=np.object_)
        return df

    def assertNaN(self, value):
        self.assertTrue(isinstance(value, numbers.Number), f"'{value}' is a {type(value)}, not a number (only numbers can be NaN)")
        self.assertTrue(math.isnan(value), f"'{value}' is not NaN")

    def assertEqualAndInt(self, expect, actual):
        self.assertEqual(expect, actual)
        self.assertEqual(int, type(actual))

