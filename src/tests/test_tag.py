from unittest import main, TestCase

from jpp.tags import Tag, Date, Verbatim, Multi


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
                self.assertEqual(None, this_tag.body)

if __name__ == "__main__":
    main()
