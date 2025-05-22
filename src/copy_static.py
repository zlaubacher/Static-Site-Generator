import os
import shutil

def copy_files_recursive(source_directory_path, destination_directory_path):
    if not os.path.exists(destination_directory_path):
        os.mkdir(destination_directory_path)
    
    for filename in os.listdir(source_directory_path):
        from_path = os.path.join(source_directory_path, filename)
        destination_path = os.path.join(destination_directory_path, filename)
        print(f" * {from_path} -> {destination_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, destination_path)
        else:
            copy_files_recursive(from_path, destination_path)