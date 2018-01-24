import unittest.mock as mock
from tests.transparency_test_case import TransparencyTestCase

import os

from transparency.downloader import Downloader


class TestDownloader(TransparencyTestCase):

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        self.downloader = Downloader()
        pass

    def tearDown(self):
        pass

    def test_download(self):
        with mock.patch('transparency.downloader.urllib.request.urlretrieve') as mock_ret:
            mock_ret.return_value = ('/tmp.txt', ['X-OK: True'])

            res = self.downloader.download('https://transparency.facebook.com/download/2013-H1/', 'tests/cache')

            mock_ret.assert_called_once_with('https://transparency.facebook.com/download/2013-H1/',
                                             'tests/cache/https___transparency_facebook_com_download_2013_H1_')
            self.assertEqual('/tmp.txt', res)

    def test_download_cached(self):
        with mock.patch('transparency.downloader.urllib.request.urlretrieve') as mock_ret:
            mock_ret.return_value = ('/tmp.txt', ['X-OK: True'])
            dir = os.path.join(os.path.dirname(__file__), 'files')

            res = self.downloader.download('file_that_exists', dir)

            mock_ret.assert_not_called()
            self.assertEqual(os.path.join(dir, 'file_that_exists'), res)

    def test_url_to_filename(self):
        got = self.downloader.url_to_filename('https://transparency.facebook.com/download/2013-H1/')
        self.assertEqual("https___transparency_facebook_com_download_2013_H1_", got)
