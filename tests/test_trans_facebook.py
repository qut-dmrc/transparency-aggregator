import unittest

from transparency.trans_facebook import TransFacebook


class TestFacebook(unittest.TestCase):
    # self.fb = None

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        self.fb = TransFacebook()

    def tearDown(self):
        pass

    def test_read_csv_from_url(self):
        self.fb.read_csv('https://transparency.facebook.com/download/2013-H1/')

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

    def test_process_urls_unreachable(self):
        unavailableURL = 'https://transparency.facebook.com.notexist/'
        available_urls = [
            {'url': unavailableURL, 'report_start': '2013-01-01 00:00:00', 'report_end': '2013-06-30 23:59:59'}]

        with self.assertLogs(level="ERROR") as cm:
            self.fb.process_urls(available_urls)
            self.assertEqual(1, len(cm.output))
            self.assertIn(f'ERROR:root:Unable to fetch url: {unavailableURL}. ', cm.output[0])


if __name__ == '__main__':
    unittest.main()
