import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a",
                        value="Click me",
                        props={"href": "https://www.google.com", "target": "_blank"}
                        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
            )
    
    def test_no_props_to_html(self):
        node = HTMLNode(tag="a",
                        value="Click me",
                        )
        self.assertEqual(
            node.props_to_html(),
            ""
            )
        
    def test_empty_props_to_html(self):
        node = HTMLNode(tag="a",
                        value="Click me",
                        props={}
                        )
        self.assertEqual(
            node.props_to_html(),
            ""
            )
        
    def test_repl(self):
        node = HTMLNode(tag="a",
                        value="Click me",
                        props={"href": "https://www.google.com", "target": "_blank"}
                        )
        self.assertEqual(
            repr(node),
            'HTMLNode("a", "Click me", None,  href="https://www.google.com" target="_blank")'
            )
        
    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This text is bold!")
        self.assertEqual(node.to_html(), "<b>This text is bold!</b>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This text is raw!")
        self.assertEqual(node.to_html(), "This text is raw!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()