import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag(self):
        node = LeafNode(None, "foobar")
        self.assertEqual(node.to_html(), "foobar")

    def test_anchor(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        node = ParentNode(None, "foo")
        with self.assertRaises(ValueError) as ve:
            node.to_html()
        self.assertEqual(str(ve.exception), "invalid HTML: no tag")

    def test_no_children(self):
        node = ParentNode("foo", None)
        with self.assertRaises(ValueError) as ve:
            node.to_html()
        self.assertEqual(str(ve.exception), "invalid HTML: no child")

    def test_children_with_no_value(self):
        node = ParentNode("p", [LeafNode("b", None)])
        with self.assertRaises(ValueError) as ve:
            node.to_html()
        self.assertEqual(str(ve.exception), "invalid HTML: no value")

    def test_children_with_value(self):
        node = ParentNode("p", [LeafNode("b", "foo")])
        self.assertEqual(node.to_html(), "<p><b>foo</b></p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()