import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("foo", TextType.BOLD)
        node2 = TextNode("foo", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("foo", TextType.BOLD, "https://foobar.com")
        node2 = TextNode("foo", TextType.BOLD, "https://foobar.com")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("foo", TextType.BOLD)
        node2 = TextNode("bar", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false_2(self):
        node = TextNode("foo", TextType.BOLD)
        node2 = TextNode("foo", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url_false(self):
        node = TextNode("foo", TextType.BOLD)
        node2 = TextNode("bar", TextType.BOLD, "https://foobar.com")
        self.assertNotEqual(node, node2)

    def test_eq_url_false_2(self):
        node = TextNode("foo", TextType.BOLD, "http://foobar.com")
        node2 = TextNode("bar", TextType.BOLD, "https://foobar.com")
        self.assertNotEqual(node, node2)

    def test_repr_url(self):
        node = TextNode("foo", TextType.LINK, "http://foobar.com")
        self.assertEqual(
            "TextNode(foo, link, http://foobar.com)", repr(node)
        )

    def test_repr(self):
        node = TextNode("foo", TextType.BOLD)
        self.assertEqual(
            "TextNode(foo, bold, None)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()