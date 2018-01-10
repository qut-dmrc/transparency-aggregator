from trans_facebook import FB

class TestFacebook(unittest.TestCase):
        # self.fb = None

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        self.fb = FB()
        self.fb.read_csv('Transparency_Reports/Facebook/Facebook-Government-Report-2013-H1.csv')

    def tearDown(self):
        pass

    def test_read_csv_fb(self):
        assert self.fb.df.size > 0

    def test_read_csv_from_url(self):
        self.fb.read_csv('https://transparency.facebook.com/download/2013-H1/')

    def test_process_fb(self):
        assert self.fb.process('2013-01-01', '2013-06-30 23:59:59').size > 0

if __name__ == '__main__':
    unittest.main()