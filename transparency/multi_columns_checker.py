"""
Check that assumptions are valid.
"""
import json

import transparency.utils as utils
from transparency.checker import Checker
import numpy as np

class MultiColumnsChecker(Checker):

    def check(self, df):
        actual_cols = df.columns.values
        actual_cols = np.array([ utils.strip_punctuation(x.lower()) for x in actual_cols ])

        expected_cols_array = self.config['expected_source_columns_array']
        expected_cols_array = [[utils.strip_punctuation(x.lower()) for x in y] for y in expected_cols_array]

        diffs = [
            self.get_diff(actual_cols, expected_cols)
            for expected_cols in expected_cols_array
        ]

        minimal_diff = min(diffs, key=lambda d: d['diff_count'])

        missing_cols = minimal_diff['missing_cols']
        extra_cols = minimal_diff['extra_cols']

        utils.check_assumption(
            (len(missing_cols) != 0) + (len(extra_cols) != 0) < 2,
            f"Unexpected missing columns ({json.dumps(missing_cols)}) " +
            f"and extra columns ({json.dumps(extra_cols)})"
        )

        utils.check_assumption(len(extra_cols) == 0, "Unexpected extra columns: " + json.dumps(extra_cols))
        utils.check_assumption(len(missing_cols) == 0, "Unexpected missing columns: " + json.dumps(missing_cols))

    def get_diff(self, actual_cols, expected_cols):
        actual_cols_set = set(actual_cols)
        expected_cols_set = set(expected_cols)
        extra_cols = list(actual_cols_set - expected_cols_set)
        missing_cols = list(expected_cols_set - actual_cols_set)
        return {
            "diff_count": len(extra_cols) + len(missing_cols),
            "missing_cols": missing_cols,
            "extra_cols": extra_cols,
            "expected_cols": expected_cols,
        }
