import unittest

from static_source import StaticSource


class TestStaticSource(unittest.TestCase):
    def setUp(self):
        self.source = StaticSource({"data": [{"url": "http://url"}]})

    def test_read_correctly_handles_numbers(self):
        data = self.source.get()
        self.assertEqual([{"url": "http://url"}], data)
