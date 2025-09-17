import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
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

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()