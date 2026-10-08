import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_default_url_is_none(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<b>bold text</b>")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<i>italic text</i>")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            "<code>print('hello')</code>",
        )

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<a href="https://www.boot.dev">Boot.dev</a>',
        )

    def test_image(self):
        node = TextNode("A description", TextType.IMAGE, "image.png")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<img src="image.png" alt="A description"></img>',
        )

    def test_invalid_type(self):
        node = TextNode("invalid", "invalid")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
