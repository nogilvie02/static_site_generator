import unittest
from block_markdown import (
    markdown_to_blocks,
    is_heading,
    is_code,
    is_quote,
    is_unordered_list,
    is_ordered_list,
    block_to_block_type,
    BlockType,
)
from markdown_to_html import markdown_to_html_node


class TestSplitDelimiter(unittest.TestCase):
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


    def test_single_block_no_blank_lines(self):
        md = "Just a single block of text with **markdown**."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single block of text with **markdown**."])


    def test_leading_and_trailing_blank_lines(self):
        md = """

First block

Second block

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])


    def test_multiple_consecutive_blank_lines(self):
        md = """First block


Second block



Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["First block", "Second block", "Third block"],
        )


    def test_only_whitespace_blocks(self):
        md = "   \n\n\t\n\nReal block\n\n  \n "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Real block"])


    def test_list_block_with_paragraph_before(self):
        md = """Intro paragraph

- item 1
- item 2
- item 3"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Intro paragraph", "- item 1\n- item 2\n- item 3"],
        )


    def test_is_heading_simple(self):
        assert is_heading("# Title") is True


    def test_is_heading_max_hashes(self):
        assert is_heading("###### Tiny") is True


    def test_is_heading_too_many_hashes(self):
        assert is_heading("####### Not heading") is False


    def test_is_heading_needs_space(self):
        assert is_heading("#NoSpace") is False


    def test_is_heading_empty_text(self):
        assert is_heading("# ") is False


    def test_is_code_simple_block(self):
        block = "```\nprint('hi')\n```"
        assert is_code(block) is True


    def test_is_code_no_newline_after_ticks(self):
        block = "```print('hi')\n```"
        assert is_code(block) is False


    def test_is_code_inline_should_fail(self):
        block = "This is ```code``` inline"
        assert is_code(block) is False


    def test_is_code_missing_closing_ticks(self):
        block = "```\nprint('hi')"
        assert is_code(block) is False


    def test_is_quote_single_line(self):
        block = "> hello there"
        assert is_quote(block) is True


    def test_is_quote_multiple_lines(self):
        block = "> first line\n> second line"
        assert is_quote(block) is True


    def test_is_quote_allows_no_space(self):
        block = ">hello\n>world"
        assert is_quote(block) is True


    def test_is_quote_line_missing_gt(self):
        block = "> valid\nnot valid"
        assert is_quote(block) is False


    def test_is_quote_empty_line_in_middle(self):
        block = "> line1\n\n> line3"
        assert is_quote(block) is False


    def test_is_unordered_list_single(self):
        block = "- item one"
        assert is_unordered_list(block) is True


    def test_is_unordered_list_multiple(self):
        block = "- item one\n- item two\n- item three"
        assert is_unordered_list(block) is True


    def test_is_unordered_list_missing_space(self):
        block = "-item one"
        assert is_unordered_list(block) is False


    def test_is_unordered_list_mixed_line(self):
        block = "- item one\nnot a list"
        assert is_unordered_list(block) is False


    def test_is_unordered_list_empty_line(self):
        block = "- item one\n"
        assert is_unordered_list(block) is False


    def test_is_ordered_list_single(self):
        block = "1. first"
        assert is_ordered_list(block) is True


    def test_is_ordered_list_multiple_correct(self):
        block = "1. first\n2. second\n3. third"
        assert is_ordered_list(block) is True


    def test_is_ordered_list_wrong_start_number(self):
        block = "2. first\n3. second"
        assert is_ordered_list(block) is False


    def test_is_ordered_list_skips_number(self):
        block = "1. first\n3. third"
        assert is_ordered_list(block) is False


    def test_is_ordered_list_missing_space(self):
        block = "1.first"
        assert is_ordered_list(block) is False


    def test_is_ordered_list_mixed_line(self):
        block = "1. first\nnot a list"
        assert is_ordered_list(block) is False


    def test_block_to_block_type_heading(self):
        block = "## Welcome"
        assert block_to_block_type(block) == BlockType.HEADING


    def test_block_to_block_type_code(self):
        block = "```\nprint('hi')\n```"
        assert block_to_block_type(block) == BlockType.CODE


    def test_block_to_block_type_quote(self):
        block = "> quoted\n> text"
        assert block_to_block_type(block) == BlockType.QUOTE


    def test_block_to_block_type_unordered_list(self):
        block = "- one\n- two"
        assert block_to_block_type(block) == BlockType.UNORDERED_LIST


    def test_block_to_block_type_ordered_list(self):
        block = "1. one\n2. two"
        assert block_to_block_type(block) == BlockType.ORDERED_LIST


    def test_block_to_block_type_paragraph(self):
        block = "Just some normal text\nthat spans multiple lines."
        assert block_to_block_type(block) == BlockType.PARAGRAPH


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()