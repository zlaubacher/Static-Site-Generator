import unittest

from md_parser import split_nodes_delimiter

from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("this is a node that has `multiple blocks` of `code text` within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 5, "failed to split the block of text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "this is a node that has ", "failed to correctly split at the first delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (first)")
        self.assertEqual(new_nodes[1].text, "multiple blocks", "failed to correctly split between the first and second delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE, "failed to label the text inside the delimiters with the proper text type (first)")
        self.assertEqual(new_nodes[2].text, " of ", "failed to correctly split between the second and third delimiters")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (second)")
        self.assertEqual(new_nodes[3].text, "code text", "failed to correctly split between the third and fourth delimiters")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE, "failed to label the text inside the delimiters with the proper text type (second)")
        self.assertEqual(new_nodes[4].text, " within it", "failed to split between the fourth delimiter and the end of the text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (third)")

    def test_bold_delimiter(self):
        node = TextNode("this is a node that has **multiple blocks** of **bold text** within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 5, "failed to split the block of text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "this is a node that has ", "failed to correctly split at the first delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (first)")
        self.assertEqual(new_nodes[1].text, "multiple blocks", "failed to correctly split between the first and second delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD, "failed to label the text inside the delimiters with the proper text type (first)")
        self.assertEqual(new_nodes[2].text, " of ", "failed to correctly split between the second and third delimiters")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (second)")
        self.assertEqual(new_nodes[3].text, "bold text", "failed to correctly split between the third and fourth delimiters")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD, "failed to label the text inside the delimiters with the proper text type (second)")
        self.assertEqual(new_nodes[4].text, " within it", "failed to split between the fourth delimiter and the end of the text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (third)")

    def test_italic_delimiter(self):
        node = TextNode("this is a node that has *multiple blocks* of *italic text* within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 5, "failed to split the block of text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "this is a node that has ", "failed to correctly split at the first delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (first)")
        self.assertEqual(new_nodes[1].text, "multiple blocks", "failed to correctly split between the first and second delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC, "failed to label the text inside the delimiters with the proper text type (first)")
        self.assertEqual(new_nodes[2].text, " of ", "failed to correctly split between the second and third delimiters")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (second)")
        self.assertEqual(new_nodes[3].text, "italic text", "failed to correctly split between the third and fourth delimiters")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC, "failed to label the text inside the delimiters with the proper text type (second)")
        self.assertEqual(new_nodes[4].text, " within it", "failed to split between the fourth delimiter and the end of the text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (third)")

    def test_multiple_delimiters(self):
        node = TextNode("this is a node that has *italic text* and `code text` as well as **bold text** all within, with extra **bold** at the end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 5, "failed to split the block of text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "this is a node that has *italic text* and `code text` as well as ", "failed to correctly split at the first delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (first)")
        self.assertEqual(new_nodes[1].text, "bold text", "failed to correctly split between the first and second delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD, "failed to label the text inside the delimiters with the proper text type (first)")
        self.assertEqual(new_nodes[2].text, " all within, with extra ", "failed to correctly split between the second and third delimiters")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (second)")
        self.assertEqual(new_nodes[3].text, "bold", "failed to correctly split between the third and fourth delimiters")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD, "failed to label the text inside the delimiters with the proper text type (second)")
        self.assertEqual(new_nodes[4].text, " at the end", "failed to split between the fourth delimiter and the end of the text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT (third)")

    def test_only_text(self):
        node = TextNode("This is just text, so nothing should split", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 1, "split the text, and it should not have")
        self.assertEqual(new_nodes[0].text, "This is just text, so nothing should split", "it split something, which is bad")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT")

    def test_leading_delimiter(self):
        node = TextNode("*This text has leading italics* within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 3, "failed to split the text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "", "there should be an empty string at the beginning")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to mark the empty text string as TextType.TEXT (first TEXT)")
        self.assertEqual(new_nodes[1].text, "This text has leading italics", "failed to properly split within the delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC, "failed to mark the content within the delimiters with the proper text type")
        self.assertEqual(new_nodes[2].text, " within it", "failed to split between the second delimiter and the end")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to mark the trailing text string as TextType.TEXT (second TEXT)")

    def test_closing_delimiter(self):
        node = TextNode("This text has *closing italics within it*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 3, "failed to split the text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "This text has ", "failed to split between the beginning and the first delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to mark the leading text string as TextType.TEXT (first TEXT)")
        self.assertEqual(new_nodes[1].text, "closing italics within it", "failed to properly split within the delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC, "failed to mark the content within the delimiters with the proper text type")
        self.assertEqual(new_nodes[2].text, "", "there should be an empty text string at the end")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to mark the empty text string as TextType.TEXT (second TEXT)")

    def test_unclosed_delimiter(self):
        with self.assertRaises(Exception) as cm:
            node = TextNode("this text has an *unclosed italic delimiter within it", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(str(cm.exception), "unclosed * delimiter within text", "failed to properly raise the exception in the event that a node was split into an even number of pieces, or that the error message was constructed correctly")

if __name__ == "__main__":
    unittest.main()