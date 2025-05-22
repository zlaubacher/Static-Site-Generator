import os
from md_parser import markdown_to_html_node

def generate_page(from_path, template_path, destination_path):
    print(f"Generating page from {from_path} to {destination_path} using {template_path}")
    from_file = open(from_path, "r")
    markdown = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", f"{title}")
    template = template.replace("{{ Content }}", html)

    destination_directory = os.path.dirname(destination_path)

    if destination_directory != "":
        os.makedirs(destination_directory, exist_ok = True)
    
    destination_file = open(destination_path, "w")
    destination_file.write(template)
    destination_file.close()

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            return title
    raise ValueError("Valid H1 title required")