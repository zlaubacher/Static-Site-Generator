import os
from md_parser import markdown_to_html_node

def generate_pages_recursive(directory_path_content, template_path, destination_directory_path):
    for entry_path in os.listdir(directory_path_content):
        current_entry_path = os.path.join(directory_path_content, entry_path)

        if os.path.isfile(current_entry_path) and current_entry_path.endswith(".md"):
            print(f"Generating page from {current_entry_path} to {destination_directory_path} using {template_path}")
            from_file = open(current_entry_path, "r")
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

            os.makedirs(destination_directory_path, exist_ok = True)
            
            public_file_name = entry_path.replace(".md", ".html")
            destination_path = os.path.join(destination_directory_path, public_file_name)

            destination_file = open(destination_path, "w")
            destination_file.write(template)
            destination_file.close()

        elif os.path.isdir(current_entry_path):
            new_destination_directory_path = os.path.join(destination_directory_path, entry_path)
            os.makedirs(new_destination_directory_path, exist_ok=True)
            generate_pages_recursive(current_entry_path, template_path, new_destination_directory_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            return title
    raise ValueError("Valid H1 title required")