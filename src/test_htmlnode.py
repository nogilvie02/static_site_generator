import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parentnode_no_tag_raises(self):
        child_node = LeafNode("i", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parentnode_no_children_raises(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_parentnode_empty_children_allowed(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_parentnode_with_props(self):
        child = LeafNode(None, "Hello")
        node = ParentNode("div", [child], {"class": "greeting"})
        self.assertEqual(node.to_html(), '<div class="greeting">Hello</div>')
    
    def test_parentnode_only_text_children(self):
        node = ParentNode("p", [LeafNode(None, "Hello"), LeafNode(None, " world")])
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_parentnode_deep_nesting(self):
        leaf = LeafNode("em", "deep")
        level3 = ParentNode("span", [leaf])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])
        self.assertEqual(
            level1.to_html(),
            "<section><div><span><em>deep</em></span></div></section>",
        )

    def test_parentnode_props_and_multiple_children(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "A"), LeafNode("span", "B")],
            {"class": "combo"},
        )
        self.assertEqual(node.to_html(), '<div class="combo">A<span>B</span></div>')

if __name__ == "__main__":
    unittest.main()