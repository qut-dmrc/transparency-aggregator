import unittest

from writer_csv import WriterCSV


class TestWriterCSV(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_abc(self):
        writer = WriterCSV({})


if __name__ == '__main__':
    unittest.main()
