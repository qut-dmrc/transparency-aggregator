from tests.transparency_test_case import TransparencyTestCase
from transparency.directory_source import DirectorySource


class TestDirectorySource(TransparencyTestCase):
    def setUp(self):
        self.source = DirectorySource(
            {"directory": "tests/files/manual/"}
        )

    def test_read_correctly_handles_numbers(self):
        data = self.source.get()
        self.assertEqual(2, len(data))
