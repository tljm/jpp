from unittest import main, TestCase

from jpp.tags import istag, maketag
from jpp.tags import Tag, Date, Verbatim, Multi

class TestHelpers(TestCase):
    
    def setUp(self):
        self.lines = """abcd
        1234
        @XYZ
        @@XYZ
        @@12341231
        @@123
        @@@
        @@""".split()
        self.tags = [0,0,0,1,1,1,1,0]
        self.types = [Multi,Date,Multi,Multi]

    def test_istag(self):
        
        for line,tag in zip(self.lines,self.tags):
            self.assertEqual(istag(line),tag==1)

    def test_maketag(self):
        
        for line,tag in zip(self.lines,self.tags):
            if istag(line):
                self.assertTrue(isinstance(maketag(line),self.types.pop(0)))


class TestTags(TestCase):

    def setUp(self):
        self.tags = (Tag, Date, Verbatim, Multi)
        self.values = (1, 'abc', None)

    def test_init(self):
        """
        Default behaviour at tag's creation.
        """
        for tag in self.tags:
            for value in self.values:
                this_tag = tag(value)
                self.assertEqual(value, this_tag.value)
                #self.assertEqual(None, this_tag.body)
                
class TestMulti(TestCase):
    
    def setUp(self):
        self.lines = """@@abc
        @@123
        @@xyz""".split()
        
        self.reference = Multi(list(map(Verbatim,[line[2:] for line in self.lines])))
        
    def test_append(self):
        tag = maketag(self.lines[0])
        tag.append(Verbatim(self.lines[1][2:]))
        for line in self.lines[2:]:
            tag.append(maketag(line))
        self.assertEqual(tag,self.reference)


if __name__ == "__main__":
    main()
