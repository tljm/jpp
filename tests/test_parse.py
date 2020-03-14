from unittest import main, TestCase

from tests.resources import get

from mdjpp.parse import JournalParser
from mdjpp.render import MD

class TestJournalParser(TestCase):

    def setUp(self):
        self.jfile = get("test_journal.mdj")

    def test_proceed(self):

        jp = JournalParser()
        #jp.engine = MD()
        
        with open(self.jfile) as jfile:
            jp.proceed(jfile)
        
if __name__ == "__main__":
    T = TestJournalParser()
    T.setUp()
    T.test_proceed()
    #main()

