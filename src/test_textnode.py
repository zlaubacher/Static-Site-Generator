import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()