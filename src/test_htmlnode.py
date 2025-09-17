import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_repr_None(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(
            "HTMLNode(None, None, None, None)", repr(node)        )


    def test_repr(self):
        node = HTMLNode("a", "foo", "bar", {"href": "https://www.google.com"})
        self.assertEqual(
            "HTMLNode(a, foo, bar, {'href': 'https://www.google.com'})", repr(node)
        )

    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(None, None, None, props)
        attributes = node.props_to_html()
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", attributes)

    def test_props_to_html_None(self):
        node = HTMLNode(None, None, None, None)
        attributes = node.props_to_html()
        self.assertEqual("", attributes)

    def test_props_to_html_value_None(self):
        props = {"href": None, "target": "_blank",}
        node = HTMLNode(None, None, None, props)
        attributes = node.props_to_html()
        self.assertEqual(" href=\"None\" target=\"_blank\"", attributes)

if __name__ == "__main__":
    unittest.main()