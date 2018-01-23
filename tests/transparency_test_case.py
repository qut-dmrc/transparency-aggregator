import textwrap
import unittest
from io import StringIO

import numpy as np
import pandas as pd


class TransparencyTestCase(unittest.TestCase):
    def get_df(self, csv):
        """
        Convert a csv string to a dataframe, ignoring whitespace from indents
        """
        df = pd.read_csv(StringIO(textwrap.dedent(csv)), encoding="UTF-8", dtype=np.object_)
        return df
