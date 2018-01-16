"""
Check that assumptions are valid.
"""
import json

import utils
from checker import Checker


class SimpleColumnsChecker(Checker):

    def check(self, df):
        expected_cols = set(self.config['expected_source_columns'])
        actual_cols = set(df.columns.values)
        extra_cols = list(actual_cols - expected_cols)
        missing_cols = list(expected_cols - actual_cols)

        utils.check_assumption(len(extra_cols) == 0, "Unexpected extra columns: " + json.dumps(extra_cols))
        utils.check_assumption(len(missing_cols) == 0, "Unexpected missing columns: " + json.dumps(missing_cols))
