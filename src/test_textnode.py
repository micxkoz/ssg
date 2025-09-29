import unittest
from textnode import *

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

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_anchor(self):
        node = TextNode("This is an anchor node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is an anchor node")
        self.assertEqual(html_node.props, {'href': 'https://google.com'})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://google.com', 'alt': 'This is an image node'})

    def test_other(self):
        node = TextNode("This is an italic node", "FOOBAR")
        self.assertRaises(Exception)

    def test_text_boot(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image_boot(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold_boot(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

if __name__ == "__main__":
    unittest.main()