from tests.transparency_test_case import TransparencyTestCase

from transparency.semiannual_url_source import SemiannualUrlSource


class TestSemiannualUrlSource(TransparencyTestCase):
    def setUp(self):
        self.source = SemiannualUrlSource({"url_template": "https://transparency.example.com/$report_year-$facebook_period-$start_month-$end_month", 'start_year': '2016', 'end_year': '2017'})

    def test_read_correctly_handles_numbers(self):
        data = self.source.get()

        expected = [
            {"url": "https://transparency.example.com/2016-H1-jan-jun", "report_start": "2016-01-01 00:00:00", "report_end": "2016-06-30 23:59:59"},
            {"url": "https://transparency.example.com/2016-H2-jul-dec", "report_start": "2016-07-01 00:00:00", "report_end": "2016-12-31 23:59:59"},
            {"url": "https://transparency.example.com/2017-H1-jan-jun", "report_start": "2017-01-01 00:00:00", "report_end": "2017-06-30 23:59:59"},
            {"url": "https://transparency.example.com/2017-H2-jul-dec", "report_start": "2017-07-01 00:00:00", "report_end": "2017-12-31 23:59:59"},
        ]

        self.assertEqual(expected, data)
