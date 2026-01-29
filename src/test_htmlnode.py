import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()