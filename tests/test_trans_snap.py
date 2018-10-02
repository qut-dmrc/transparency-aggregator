from transparency.trans_snap_removal import TransSnapRemoval
from tests.transparency_test_case import TransparencyTestCase


class TestSnap(TransparencyTestCase):
    def setUp(self):
        self.snap_removal = TransSnapRemoval()

    def test_government_removals(self):
        available_urls = [{
                              'url': 'https://www.snap.com/en-US/privacy/transparency/',
                              'report_start': '2017-07-01 00:00:00', 'report_end': '2017-12-31 23:59:59'}]
        df_out = self.snap_removal.process_urls(available_urls)
        self.assertEqual('Saudi Arabia', df_out['country'][0])
        self.assertEqual(1, df_out['num_requests'][2])
        self.assertEqual(1, df_out['num_requests_complied'][2])
