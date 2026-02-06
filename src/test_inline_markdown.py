import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images
from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is a **bold** node", TextType.TEXT)
        new_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), new_nodes)

    def test_split_italic(self):
        node = TextNode("This is an _italic_ node", TextType.TEXT)
        new_nodes = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), new_nodes)

    def test_split_code(self):
        node = TextNode("This is a `code` node", TextType.TEXT)
        new_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), new_nodes)

    def test_split_multi_bold(self):
        node = TextNode("This is a **bold** node with **multiple bold** texts", TextType.TEXT)
        new_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node with ", TextType.TEXT),
            TextNode("multiple bold", TextType.BOLD),
            TextNode(" texts", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), new_nodes)

    def test_split_no_bold(self):
        node = TextNode("This is not a bold node", TextType.TEXT)
        new_nodes = [
            TextNode("This is not a bold node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), new_nodes)

    def test_split_wrong_delimiter(self):
        node = TextNode("This is not a `bold` node", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()