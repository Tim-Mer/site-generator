import unittest

from blocks import *

class TestTextNode(unittest.TestCase):
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
        
    def test_markdown_to_blocks_extra_newlines(self):
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
    
    def test_markdown_to_blocks_single_paragraph(self):
        md = "This is a single paragraph with no extra newlines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no extra newlines."])

    def test_markdown_to_blocks_multiple_paragraphs(self):
        md = """
This is the first paragraph.

This is the second paragraph.

This is the third paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the first paragraph.",
                "This is the second paragraph.",
                "This is the third paragraph.",
            ],
        )

    def test_markdown_to_blocks_list_items(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2\n- Item 3"])

    def test_markdown_to_blocks_mixed_content(self):
        md = """
This is a paragraph.

- Item 1
- Item 2

Another paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "- Item 1\n- Item 2",
                "Another paragraph.",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_paragraph_with_extra_spaces(self):
        md = "   This is a paragraph with leading and trailing spaces.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with leading and trailing spaces."])
        
    def test_block_to_blocktype_h1(self):
        md = "# h1 heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
    
    def test_block_to_blocktype_h2(self):
        md = "## h2 heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
    
    def test_block_to_blocktype_h3(self):
        md = "### h3 heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
    
    def test_block_to_blocktype_h4(self):
        md = "#### h4 heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
    
    def test_block_to_blocktype_h5(self):
        md = "##### h5 heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
    
    def test_block_to_blocktype_h6(self):
        md = "###### h6 heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
        
    def test_block_to_blocktype_paragraph(self):
        md = """This is a paragraph
with
lots
of 
information!"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)
        
    def test_block_to_blocktype_code(self):
        md = """```
Some code
print("Hello World")
```"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.CODE)
        
    def test_block_to_blocktype_quote(self):
        md = "> This is a quote"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.QUOTE)
        
    def test_block_to_blocktype_unordered_list(self):
        md = """- This
- Is
- An
- Unordered
- List"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.UNORDERED_LIST)
        
    def test_block_to_blocktype_ordered_list(self):
        md = """1. This
2. List
3. Is
4. Ordered"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.ORDERED_LIST)
    
    def test_block_to_blocktype_mixed_list(self):
        md = """- Item 1
- Item 2
1. Ordered item 1
2. Ordered item 2"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)  # Mixed lists are treated as paragraphs

#    def test_block_to_blocktype_code_with_language(self):
#        md = """```python
#print("Hello World")
#```"""
#        type = block_to_block_type(md)
#        self.assertEqual(type, BlockType.CODE)

    def test_block_to_blocktype_multiline_quote(self):
        md = """> This is a multiline
> quote that spans
> multiple lines."""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list_with_indentation(self):
        md = """- Item 1
  - Subitem 1
  - Subitem 2"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_heading_with_extra_spaces(self):
        md = "   ### Heading with spaces   "
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
        
if __name__ == "__main__":
    unittest.main()