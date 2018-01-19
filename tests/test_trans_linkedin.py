import textwrap
import unittest
from io import StringIO

import numpy as np
import pandas as pd

from transparency.trans_linkedin import TransLinkedin


class TestTransLinkedin(unittest.TestCase):
    def setUp(self):
        self.trans = TransLinkedin()

    def tearDown(self):
        pass

    def sample_df(self):
        csv = \
            """
            accountsImpacted,country,memberDataRequests,percentProvided,report_end,report_start,subjectToRequest,isMLAT
            ,India,12,11%,2011-12-31 23:59:59,2011-07-01 00:00:00,13,
            ,United States,22,21%,2011-12-31 23:59:59,2011-07-01 00:00:00,23,
            31,India,33,32%,2012-06-30 23:59:59,2012-01-01 00:00:00,34,True
            """

        df = pd.read_csv(StringIO(textwrap.dedent(csv)), encoding="UTF-8", dtype=np.object_)
        return df

    def test_process_with_check_should_load_data(self):
        df = self.sample_df()
        df_out = self.trans.process_with_check(df, '', '')
        self.assertEqual('India', df_out['country'][0])
        self.assertEqual(12, df_out['num_requests'][0])


if __name__ == '__main__':
    unittest.main()
