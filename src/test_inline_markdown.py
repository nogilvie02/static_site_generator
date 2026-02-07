import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_at_beginning(self):
        node = TextNode(
            "![Image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" afterwards", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "No images to split in this node",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("No images to split in this node", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "before ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_ignores_non_text(self):
        img_node = TextNode("alt", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        new_nodes = split_nodes_image([img_node])
        self.assertListEqual([img_node], new_nodes)

    def test_split_images_multiple_nodes(self):
        n1 = TextNode(
            "First ![one](url1)", TextType.TEXT
        )
        n2 = TextNode(
            "Second with no image", TextType.TEXT
        )
        new_nodes = split_nodes_image([n1, n2])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode("Second with no image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.TEXT)], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes,
        )

    def test_split_links_again(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_links_at_beginning(self):
        node = TextNode(
            "[First](https://www.boot.dev) and another [second](https://www.google.com) afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://www.google.com"),
                TextNode(" afterwards", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode(
            "before [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode(
            "[link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
            "No links to split in this node",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("No links to split in this node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_ignores_non_text(self):
        link_node = TextNode("boot dev", TextType.LINK, "https://www.boot.dev")
        new_nodes = split_nodes_link([link_node])
        self.assertListEqual([link_node], new_nodes)

    def test_split_links_multiple_nodes(self):
        n1 = TextNode("First [one](url1)", TextType.TEXT)
        n2 = TextNode("Second with no link", TextType.TEXT)
        new_nodes = split_nodes_link([n1, n2])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.LINK, "url1"),
                TextNode("Second with no link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_no_links_bold(self):
        node = TextNode(
            "No links to split in this node",
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("No links to split in this node", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_plain_text(self):
        nodes = text_to_textnodes("Just some plain text.")
        self.assertListEqual(
            [TextNode("Just some plain text.", TextType.TEXT)],
            nodes,
        )

    def test_text_to_textnodes_only_bold(self):
        nodes = text_to_textnodes("Start **bold** end")
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" end", TextType.TEXT),
            ],
            nodes
        )

    def test_text_to_textnodes_images_and_links(self):
        nodes = text_to_textnodes(
            "![img1](http://a.com) and [link](http://b.com) and ![img2](http://c.com)"
        )
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "http://a.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://b.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "http://c.com"),
            ],
            nodes
        )

    def test_text_to_textnodes_unmatched_bold_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("These ** are not _real_ markers `here")

if __name__ == "__main__":
    unittest.main()