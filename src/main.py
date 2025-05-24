import os
import shutil
from copy_static import copy_files_recursive
from generate import generate_pages_recursive

directory_path_static = "./static"
directory_path_public = "./public"
directory_path_content = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(directory_path_public):
        shutil.rmtree(directory_path_public)
        print("DEBUG: public directory deleted.")
    
    print("Copying files from static storage to public directory...")
    copy_files_recursive(directory_path_static, directory_path_public)

    generate_pages_recursive(directory_path_content, template_path, directory_path_public)

main()