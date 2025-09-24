import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

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

class TestInlineMarkdown(unittest.TestCase):
    def test_specification(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_not_applicable_delimiter(self):
        node = TextNode("foobar", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("foobar", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_empty_node(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        expected_result = []
        self.assertEqual(new_nodes, expected_result)


    def test_other_texttype(self):
        node = TextNode("f`ooba`r", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("f`ooba`r", TextType.CODE)
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_invalid_markdown(self):
        node = TextNode("f`oo`ba`r", TextType.TEXT)
        with self.assertRaises(ValueError) as ve:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(ve.exception), "invalid Markdown")

    def test_invalid_markdown_2(self):
        node = TextNode("foo`bar", TextType.TEXT)
        with self.assertRaises(ValueError) as ve:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(ve.exception), "invalid Markdown")

    def test_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_italic(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_result = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.ITALIC),
        TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_no_first_part(self):
        node = TextNode("**This is text with** a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
        TextNode("This is text with", TextType.BOLD),
        TextNode(" a code block word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()