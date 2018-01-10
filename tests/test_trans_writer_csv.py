import unittest
from trans_writer_csv import TransparencyWriterCSV

class TestTransparencyWriterCSV(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass    

    def setUp(self): 
        pass

    def tearDown(self):
        pass    

    def test_abc(self):
        writer = TransparencyWriterCSV()

if __name__ == '__main__':
    unittest.main()