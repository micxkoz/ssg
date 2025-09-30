import unittest
from blockmarkdown import *

class TestSplitBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph


   foobar   


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "foobar",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockTypes(unittest.TestCase):
    def test_heading1(self):
        block = "# foo"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading2(self):
        block = "## foo"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading3(self):
        block = "### foo"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading4(self):
        block = "#### foo"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading5(self):
        block = "##### foo"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading6(self):
        block = "###### foo"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading7(self):
        block = "####### foo"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_onlyhashes(self):
        block = "###"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_nospace(self):
        block = "###foo"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```foobar```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_bad(self):
        block = "```foobar`"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_bad2(self):
        block = "`foobar```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_bad3(self):
        block = "``````"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> asdf\n> asdf\n> asdf"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_bad(self):
        block = "> asdf\n asdf"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote2(self):
        block = ">asdf\n> asdf"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- asdf\n- asdf\n- asdf"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_bad(self):
        block = "- asdf\n asdf"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_bad2(self):
        block = "- asdf\n-asdf"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. asdf\n2. asdf\n3. asdf"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_bad_1(self):
        block = "1. asdf\n2.asdf"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_bad_2(self):
        block = "1. asdf\n2 asdf"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_bad_3(self):
        block = "1. asdf\n. asdf"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_bad_4(self):
        block = "1. asdf\n2. asdf\n2. asdf"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()