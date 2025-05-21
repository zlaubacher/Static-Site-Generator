import os
import shutil


directory_path_static = "./static"
directory_path_public = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(directory_path_public):
        shutil.rmtree(directory_path_public)
    

main()