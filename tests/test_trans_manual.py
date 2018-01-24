import textwrap
from io import StringIO

import numpy as np
import pandas as pd

from tests.transparency_test_case import TransparencyTestCase
from transparency.trans_manual import TransManual


class TestTransManual(TransparencyTestCase):

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        self.trans = TransManual()

    def tearDown(self):
        pass

    def sample_df(self):
        csv = \
            """
            "report_start","report_end","platform","property","country","request_type","request_subtype","num_requests","num_accounts_specified","num_requests_complied","num_accounts_complied","agency","reason"
            "2013-01-01 00:00:00","2013-06-30 23:59:59","Fake Company Inc.","Fake Property","Albania","requests for user data","all","10","20","30","40","",""
            """

        df = pd.read_csv(StringIO(textwrap.dedent(csv)), encoding="UTF-8", dtype=np.object_)
        return df

    def test_process_with_check_should_load_data(self):
        df = self.sample_df()
        df_out = self.trans.process_with_check(df, '', '')
        self.assertEqual('Albania', df_out['country'][0])
