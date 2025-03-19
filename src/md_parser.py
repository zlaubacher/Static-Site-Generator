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