from transparency.trans_facebook import TransFacebook
from tests.transparency_test_case import TransparencyTestCase


class TestFacebook(TransparencyTestCase):
    def setUp(self):
        self.fb = TransFacebook()

    def test_read_loads_csv_from_url(self):
        self.fb.read('https://transparency.facebook.com/download/2013-H1/')

    def test_get_urls(self):
        start_year = 2013
        end_year = 2014

        available_urls = self.fb.get_urls(start_year, end_year)

        self.assertEqual(4, len(available_urls))
        self.assertEqual('https://transparency.facebook.com/download/2013-H1/', available_urls[0]['url'])
        self.assertEqual('2013-01-01 00:00:00', available_urls[0]['report_start'])
        self.assertEqual('2013-06-30 23:59:59', available_urls[0]['report_end'])

        self.assertEqual('https://transparency.facebook.com/download/2014-H2/', available_urls[3]['url'])
        self.assertEqual('2014-07-01 00:00:00', available_urls[3]['report_start'])
        self.assertEqual('2014-12-31 23:59:59', available_urls[3]['report_end'])

    def test_process_urls(self):
        available_urls = [
            {'url': 'https://transparency.facebook.com/download/2013-H1/', 'report_start': '2013-01-01 00:00:00',
             'report_end': '2013-06-30 23:59:59'}]

        self.fb.process_urls(available_urls)

    def sample_df(self):
        return self.get_df(
            """
            Country,"Total Requests for User Data","Total User Accounts Referenced","Total Percentage of Requests Where Some Data Produced","Content Restrictions","Preservations Requested","Users/Accounts Preserved"
            Argentina,100,"200",50.00%,10,800,900
            """
        )

    def test_process_preservation_requests_are_translated_correctly(self):
        df_out = self.fb.process(self.sample_df(), '2017-01-01 00:00:00', '2017-06-30 23:59:59')
        self.assertEqual(3, df_out.shape[0])

        row = df_out.query('country=="Argentina" and request_type=="preservation requests"').iloc[0]

        self.assertEqual('Argentina', row['country'])
        self.assertEqual(800, row['num_requests'])
        self.assertEqual(900, row['num_accounts_specified'])
        self.assertIsNone(row['num_accounts_complied'])
        self.assertIsNone(row['num_requests_complied'])
        self.assertEqual('preservation requests', row['request_subtype'])
        self.assertEqual('preservation requests', row['request_type'])

    def test_process_urls_unreachable(self):
        unavailableURL = 'https://transparency.facebook.com.notexist/'
        available_urls = [
            {'url': unavailableURL, 'report_start': '2013-01-01 00:00:00', 'report_end': '2013-06-30 23:59:59'}]

        with self.assertLogs(level="ERROR") as cm:
            self.fb.process_urls(available_urls)
            self.assertEqual(1, len(cm.output))
            self.assertIn(f'ERROR:root:Unable to fetch url: {unavailableURL}. ', cm.output[0])
