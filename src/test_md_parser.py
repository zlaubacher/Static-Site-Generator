import unittest

from md_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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
        node = TextNode("this is a node that has _multiple blocks_ of _italic text_ within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

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
        node = TextNode("this is a node that has _italic text_ and `code text` as well as **bold text** all within, with extra **bold** at the end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 5, "failed to split the block of text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "this is a node that has _italic text_ and `code text` as well as ", "failed to correctly split at the first delimiter")
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
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 1, "split the text, and it should not have")
        self.assertEqual(new_nodes[0].text, "This is just text, so nothing should split", "it split something, which is bad")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to properly separate non formatted text as TextType.TEXT")

    def test_leading_delimiter(self):
        node = TextNode("_This text has leading italics_ within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 3, "failed to split the text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "", "there should be an empty string at the beginning")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to mark the empty text string as TextType.TEXT (first TEXT)")
        self.assertEqual(new_nodes[1].text, "This text has leading italics", "failed to properly split within the delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC, "failed to mark the content within the delimiters with the proper text type")
        self.assertEqual(new_nodes[2].text, " within it", "failed to split between the second delimiter and the end")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to mark the trailing text string as TextType.TEXT (second TEXT)")

    def test_closing_delimiter(self):
        node = TextNode("This text has _closing italics within it_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 3, "failed to split the text into the correct number of pieces")
        self.assertEqual(new_nodes[0].text, "This text has ", "failed to split between the beginning and the first delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT, "failed to mark the leading text string as TextType.TEXT (first TEXT)")
        self.assertEqual(new_nodes[1].text, "closing italics within it", "failed to properly split within the delimiters")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC, "failed to mark the content within the delimiters with the proper text type")
        self.assertEqual(new_nodes[2].text, "", "there should be an empty text string at the end")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT, "failed to mark the empty text string as TextType.TEXT (second TEXT)")

    def test_unclosed_delimiter(self):
        with self.assertRaises(Exception) as cm:
            node = TextNode("this text has an _unclosed italic delimiter within it", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(str(cm.exception), "unclosed _ delimiter within text", "failed to properly raise the exception in the event that a node was split into an even number of pieces, or that the error message was constructed correctly")

class TestImageExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches, "failed to correctly extract image URLs and their alt text")

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images("This is text with two images ![image1](image1 url), and ![image2](image2 url)")
        self.assertListEqual([("image1", "image1 url"), ("image2", "image2 url")], matches, "failed to correctly extract image URLs and their alt text")

class TestLinkExtractor(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](www.google.com)")
        self.assertListEqual([("link", "www.google.com")], matches, "failed to correctly extract link URLs and their alt text")

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links("This is text with two links [link1](link1 url), and [link2](link2 url)")
        self.assertListEqual([("link1", "link1 url"), ("link2", "link2 url")], matches, "failed to correctly extract link URLs and their alt text")

    def test_extract_markdown_link_with_image(self):
        matches = extract_markdown_links("This is text with a link and an image ![image](image url), and [link](link url)")
        self.assertListEqual([("link", "link url")], matches, "failed to correctly extract link URLs and their alt text when in the presence of an image to throw the regex off")

class TestImageNodeSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT
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
        "failed to properly split the block of text in correct places (there were two images within the example)"
        )
    
    def test_no_markdown(self):
        node = TextNode("this is text without any images to check and make sure it's still handled correctly.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("this is text without any images to check and make sure it's still handled correctly.", TextType.TEXT)], new_nodes, "the function should have done nothing to this test and appended it to the list as is")
    
    def test_leading_image(self):
        node = TextNode("![A leading image](https://i.imgur.com/zjjcJKZ.png) begins this block of text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("A leading image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" begins this block of text.", TextType.TEXT)], new_nodes, "failed to properly split a block of text with a leading image")

    def test_trailing_image(self):
        node = TextNode("This block of text ends with ![a trailing image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This block of text ends with ", TextType.TEXT), TextNode("a trailing image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes, "failed to properly split a block of text with a trailing image")

class TestLinkNodeSplit(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        "failed to properly split the block of text in correct places (there were two links within the example)"
        )
    
    def test_no_markdown(self):
        node = TextNode("this is text without any links to check and make sure it's still handled correctly.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("this is text without any links to check and make sure it's still handled correctly.", TextType.TEXT)], new_nodes, "the function should have done nothing to this test and appended it to the list as is")

    def test_leading_link(self):
        node = TextNode("[A leading link](https://i.imgur.com/zjjcJKZ.png) begins this block of text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("A leading link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" begins this block of text.", TextType.TEXT)], new_nodes, "failed to properly split a block of text with a leading link")

    def test_trailing_link(self):
        node = TextNode("This block of text ends with [a trailing link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This block of text ends with ", TextType.TEXT), TextNode("a trailing link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")], new_nodes, "failed to properly split a block of text with a trailing link")

if __name__ == "__main__":
    unittest.main()