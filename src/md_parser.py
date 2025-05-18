import re
from textnode import TextNode, TextType

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