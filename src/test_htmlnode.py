import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_basicinit(self):
        node = HTMLNode()
        self.assertIsNone(node.tag, "Expected default tag to be None")
        self.assertIsNone(node.value, "Expected default value to be None")
        self.assertIsNone(node.children, "Expected default children to be None")
        self.assertIsNone(node.props, "Expected default props to be None")

    def test_withvalues(self):
        tag = "a tag"
        value = "a value"
        children = [HTMLNode(tag = "span", value = "child")]
        props = {"class": "main", "id": "paragraph1"}
        node = HTMLNode(tag = tag, value = value, children = children, props = props)

        self.assertEqual(node.tag, tag, "Tag should be set correctly")
        self.assertEqual(node.value, value, "Value should be set correctly")
        self.assertEqual(node.children, children, "Children should be set correctly")
        self.assertEqual(node.props, props, "Props should be set correctly")

    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "", "Expected empty string when props is None")

        props = {"href": "https://example.com", "target": "_blank"}
        node_with_props = HTMLNode(props=props)
        self.assertEqual(node_with_props.props_to_html(), ' href="https://example.com" target="_blank"', "Expected HTML attributes string when props are provided")

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_props(self):
        props = {"href": "https://example.com", "target": "_blank"}
        node = LeafNode("a", "Click here", props=props)
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click here</a>')

    def test_leaf_node_without_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_node_without_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_html_generation(self):
        child_node = LeafNode("span", "child content")
        parent_node = ParentNode("div", [child_node])

        expected_html = "<div><span>child content</span></div>"
        self.assertEqual(parent_node.to_html(), expected_html, "parent node to html method did not generate expected output")
    
    def test_nested_children(self):
        grandchild_node = LeafNode("b", "grandchild content")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        expected_html = "<div><span><b>grandchild content</b></span></div>"
        self.assertEqual(parent_node.to_html(), expected_html, "parent node failed to properly construct html from nested children")
    
    def test_same_level_children(self):
        child1 = LeafNode("i", "Rei")
        child2 = LeafNode("b", "Asuka")
        child3 = LeafNode("span", "Shinji")
        parent_node = ParentNode("div", [child1, child2, child3])

        expected_html = "<div><i>Rei</i><b>Asuka</b><span>Shinji</span></div>"
        self.assertEqual(parent_node.to_html(), expected_html, "parent node failed to properly construct html from multiple children on same level of nesting")
    
    def test_missing_tag(self):
        with self.assertRaises(ValueError) as cm:
            parent_node = ParentNode(None, [LeafNode("span", "child content")])
            parent_node.to_html()

        self.assertEqual(str(cm.exception), "ParentNode must have a tag", "value error was not properly raised in absence of a tag")
    
    def test_empty_children(self):
        with self.assertRaises(ValueError) as cm:
            parent_node = ParentNode("div", [])
            parent_node.to_html()

        self.assertEqual(str(cm.exception), "ParentNode must have children", "value error was not properly raised for empty children")
    
    def test_missing_tag_and_children(self):
        with self.assertRaises(ValueError) as cm:
            parent_node = ParentNode(None, None)
            parent_node.to_html()

        self.assertEqual(str(cm.exception), "ParentNode must have a tag; ParentNode must have children", "value error was not properly raised for missing tag and children")

if __name__ == "__main__":
    unittest.main()