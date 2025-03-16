import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("some text", TextType.BOLD)
        node2 = TextNode("some text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_urlnone(self):
        node = TextNode("some text", TextType.TEXT)
        self.assertIsNone(node.url)
    def test_texttypesame(self):
        node = TextNode("some text", TextType.TEXT)
        node2 = TextNode("some other text", TextType.TEXT)
        self.assertEqual(node.text_type, node2.text_type)
    def test_texttypedif(self):
        node = TextNode("some text", TextType.BOLD)
        node2 = TextNode("some other text", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    def test_italics(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    def test_link(self):
        node = TextNode("click me", TextType.LINK)
        node.url = "https://example.com"
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click me")
        self.assertEqual(html_node.props["href"], "https://example.com")
    def test_img(self):
        node = TextNode("some alt text", TextType.IMAGE)
        node.url = "https://example.com/img.jpg"
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/img.jpg")
        self.assertEqual(html_node.props["alt"], "some alt text")
    def test_invalid_text_type(self):
        node = TextNode("invalid type node", "INVALID_TYPE")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "invalid text type")

if __name__ == "__main__":
    unittest.main()