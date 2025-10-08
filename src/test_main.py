import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_specification(self):
        node = "# Hello"
        self.assertEqual(extract_title(node), "Hello")

    def test_bad_header(self):
        node = "#Hello"
        with self.assertRaises(Exception) as e:
            extract_title(node)
        self.assertEqual(str(e.exception), "Missing header with title")

    def test_no_title_header(self):
        node = "## Hello"
        with self.assertRaises(Exception) as e:
            extract_title(node)
        self.assertEqual(str(e.exception), "Missing header with title")

    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
"""
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass

    def test_eq_first_is_bad(self):
        actual = extract_title(
            """
## This is not a title

# This is a title
"""
        )
        self.assertEqual(actual, "This is a title")


if __name__ == "__main__":
    unittest.main()