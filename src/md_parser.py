import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"unclosed {delimiter} delimiter within text")
        
        processed_nodes = []

        for i, part in enumerate(parts):
            if i % 2 == 0:
                processed_nodes.append(TextNode(part, TextType.TEXT))
            else:
                processed_nodes.append(TextNode(part, text_type))
        
        new_nodes.extend(processed_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"

            parts = remaining_text.split(image_markdown, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        for anchor_text, url in links:
            link_markdown = f"[{anchor_text}]({url})"

            parts = remaining_text.split(link_markdown, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    list_in_progress = [TextNode(text, TextType.TEXT)]

    list_in_progress = split_nodes_image(list_in_progress)
    list_in_progress = split_nodes_link(list_in_progress)
    list_in_progress = split_nodes_delimiter(list_in_progress, "`", TextType.CODE)
    list_in_progress = split_nodes_delimiter(list_in_progress, "**", TextType.BOLD)
    list_in_progress = split_nodes_delimiter(list_in_progress, "_", TextType.ITALIC)
    
    return list_in_progress

def markdown_to_blocks(markdown):
    cleaned_markdown = markdown.strip()
    processing = cleaned_markdown.split("\n\n")
    blocks = []
    for block in processing:
        block = block.strip()
        if block:
            blocks.append(block)
    return blocks

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ",)):
        return BlockType.HEAD
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARA
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARA
        return BlockType.ULIST
    if block.startswith("1."):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}."):
                return BlockType.PARA
            i += 1
        return BlockType.OLIST
    return BlockType.PARA

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARA:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEAD:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def olist_to_html_node(block):
    lines = block.split("\n")
    html_lines = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        html_lines.append(ParentNode("li", children))
    return ParentNode("ol", html_lines)

def ulist_to_html_node(block):
    lines = block.split("\n")
    html_lines = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_lines.append(ParentNode("li", children))
    return ParentNode("ul", html_lines)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])