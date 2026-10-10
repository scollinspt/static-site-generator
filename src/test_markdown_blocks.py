import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_removes_excessive_blank_lines(self):
        markdown = "first\n\n\n\nsecond"
        self.assertEqual(markdown_to_blocks(markdown), ["first", "second"])

    def test_strips_block_whitespace(self):
        markdown = "  first block  \n\n\tsecond block\n"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["first block", "second block"],
        )

    def test_empty_document(self):
        self.assertEqual(markdown_to_blocks(" \n\n\t"), [])


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        for level in range(1, 7):
            self.assertEqual(
                block_to_block_type(f"{'#' * level} heading"),
                BlockType.HEADING,
            )

    def test_invalid_headings_are_paragraphs(self):
        self.assertEqual(block_to_block_type("####### heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##heading"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"),
            BlockType.CODE,
        )
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> first\n>second"),
            BlockType.QUOTE,
        )
        self.assertEqual(
            block_to_block_type("> first\nnot quoted"),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- first\n- second"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("- first\nsecond"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("1. first\n3. third"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("2. second\n3. third"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("A normal paragraph\nwith another line"),
            BlockType.PARAGRAPH,
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        markdown = """This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here"""
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        markdown = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        markdown = "# First **heading**\n\n###### Sixth heading"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><h1>First <b>heading</b></h1>"
            "<h6>Sixth heading</h6></div>",
        )

    def test_quote(self):
        markdown = "> A quote with _style_\n> across two lines"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><blockquote>A quote with <i>style</i> across two lines"
            "</blockquote></div>",
        )

    def test_lists(self):
        markdown = """- first **item**
- second item

1. first item
2. second `item`"""
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><ul><li>first <b>item</b></li><li>second item</li></ul>"
            "<ol><li>first item</li><li>second <code>item</code></li></ol></div>",
        )

    def test_multiline_paragraph(self):
        markdown = "first line\nsecond line"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><p>first line second line</p></div>",
        )


if __name__ == "__main__":
    unittest.main()