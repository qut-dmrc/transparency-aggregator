from tests.transparency_test_case import TransparencyTestCase

from transparency.static_source import StaticSource


class TestStaticSource(TransparencyTestCase):
    def setUp(self):
        self.source = StaticSource({"data": [{"url": "http://url"}]})

    def test_read_correctly_handles_numbers(self):
        data = self.source.get()
        self.assertEqual([{"url": "http://url"}], data)
