from transparency.trans_snap import TransSnap
from tests.transparency_test_case import TransparencyTestCase


class TestFacebook(TransparencyTestCase):
    def setUp(self):
        self.snap = TransSnap()

    def test_government_removals(self):
        available_urls = [{
                              'url': 'https://www.snap.com/en-US/privacy/transparency/',
                              'report_start': '2017-01-01 00:00:00', 'report_end': '2017-06-30 23:59:59'}]
        df_out = self.snap.process_urls(available_urls)
        self.assertEqual('Saudi Arabia', df_out['country'][2])
        self.assertEqual(1, df_out['num_requests'][2])
        self.assertEqual(1, df_out['num_requests_complied'][2])
