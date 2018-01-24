from tests.transparency_test_case import TransparencyTestCase

from transparency.writer_csv import WriterCSV


class TestWriterCSV(TransparencyTestCase):

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
