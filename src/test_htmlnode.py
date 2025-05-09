import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq_props(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')
    
    def test_neq_props(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), 'href="https://www.boot.dev" target="_blank"')
        
    def test_eq_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')
        
    def test_eq(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), "HTMLNode(a, Google, None, {'href': 'https://www.google.com', 'target': '_blank'})")
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
        
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_node_with_deeply_nested_children(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), 'ParentNode is missing children')

    def test_parent_node_with_invalid_children_type(self):
        with self.assertRaises(ValueError) as cm:
            parent_node = ParentNode("div", "not_a_list")
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode is missing children")

    def test_parent_node_with_missing_tag(self):
        with self.assertRaises(ValueError) as cm:
            parent_node = ParentNode(None, [LeafNode("span", "child")])
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode is missing tag")

    def test_leaf_node_with_invalid_value_type(self):
        with self.assertRaises(ValueError) as cm:
            leaf_node = LeafNode("p", 123)
            leaf_node.to_html()
        self.assertEqual(str(cm.exception), "Leaf is missing value")

    def test_leaf_node_with_no_tag(self):
        leaf_node = LeafNode(None, "Hello, world!")
        self.assertEqual(leaf_node.to_html(), "Hello, world!")

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>",
        )

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("a", "Google", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_parent_node_with_props(self):
        child = LeafNode("span", "child")
        parent_node = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_leaf_node_with_props(self):
        leaf_node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(
            leaf_node.to_html(),
            '<img src="image.jpg" alt="An image"></img>',
        )


if __name__ == "__main__":
    unittest.main()