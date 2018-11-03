from unittest import main, TestCase

from tests.resources import get

from mdjpp.parse import JournalParser

class TestJournalParser(TestCase):

    def setUp(self):
        self.jfile = get("test_journal.mdj")

    def test_proceed(self):

        jp = JournalParser()
        
        with open(self.jfile) as jfile:
            jp.proceed(jfile)
        
if __name__ == "__main__":
    main()

