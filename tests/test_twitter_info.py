from tests.transparency_test_case import TransparencyTestCase

from transparency.twitter_info import TransTwitterInfo


class TestTransTwitter(TransparencyTestCase):
    # self.twitter = None

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        self.twitter = TransTwitterInfo()

    def tearDown(self):
        pass

    def test_get_urls(self):
        start_year = 2013
        end_year = 2014

        available_urls = self.twitter.get_urls(start_year, end_year)

        self.assertEqual(4, len(available_urls))
        self.assertEqual(
            'https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-jan-jun-2013.csv',
            available_urls[0]['url'])
        self.assertEqual('2013-01-01 00:00:00', available_urls[0]['report_start'])
        self.assertEqual('2013-06-30 23:59:59', available_urls[0]['report_end'])

        self.assertEqual(
            'https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-jul-dec-2014.csv',
            available_urls[3]['url'])
        self.assertEqual('2014-07-01 00:00:00', available_urls[3]['report_start'])
        self.assertEqual('2014-12-31 23:59:59', available_urls[3]['report_end'])

    def test_process_urls(self):
        available_urls = [{
                              'url': 'https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-jan-jun-2017.csv',
                              'report_start': '2017-01-01 00:00:00', 'report_end': '2017-06-30 23:59:59'}]
        df_out = self.twitter.process_urls(available_urls)
        self.assertEqual('Australia', df_out['country'][2])
        self.assertEqual(14, df_out['num_requests'][2])
        self.assertEqual(6, df_out['num_requests_complied'][2])
        self.assertEqual(20, df_out['num_accounts_specified'][2])

    def test_process_urls_should_remove_total_column(self):
        available_urls = [{
            'url': 'https://transparency.twitter.com/content/dam/transparency-twitter/data/download-govt-information-requests/information-requests-report-jan-jun-2017.csv',
            'report_start': '2017-01-01 00:00:00', 'report_end': '2017-06-30 23:59:59'}]
        df_out = self.twitter.process_urls(available_urls)

        self.assertEqual(0, len(df_out.query('country=="TOTAL"')))
