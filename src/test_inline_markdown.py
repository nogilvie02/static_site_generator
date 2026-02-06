import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/fJRm4Vk.jpeg) too"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("another image", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_no_markdown_images(self):
        matches = extract_markdown_images(
            "This is text without a properly formatted image https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_no_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a properly formatted link to boot dev https://www.boot.dev and to youtube https://www.youtube.com/@bootdotdev"
        )
        self.assertListEqual([], matches)

    def test_extract_no_markdown_link_with_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_at_start(self):
        matches = extract_markdown_links(
            "[Starting Link](https://start.com) and some text."
        )
        self.assertListEqual([("Starting Link", "https://start.com")], matches)

if __name__ == "__main__":
    unittest.main()