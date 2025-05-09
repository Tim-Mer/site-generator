import unittest

from generate import *


class TestHTMLNode(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Hello
end
"""
        self.assertEqual(
            extract_title(md),
            "Hello",
        )

    def test_extract_title_with_multiple_headings(self):
        md = """
# First Title
## Second Title
### Third Title
"""
        self.assertEqual(
            extract_title(md),
            "First Title",
        )

    def test_extract_title_with_whitespace(self):
        md = """
        
# Title with leading whitespace
        
"""
        self.assertEqual(
            extract_title(md),
            "Title with leading whitespace",
        )

    def test_extract_title_with_special_characters(self):
        md = """
# Title with !@#$%^&*() special characters
"""
        self.assertEqual(
            extract_title(md),
            "Title with !@#$%^&*() special characters",
        )


if __name__ == "__main__":
    unittest.main()