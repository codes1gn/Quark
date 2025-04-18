
import os
import re


def replace_in_file(file_path, old_str, new_str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = re.sub(old_str, new_str, content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except UnicodeDecodeError:
        print(f"Skipping binary or non-utf-8 file: {file_path}")

def replace_in_filenames_and_contents(folder_path, old_str, new_str):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        # Rename files
        for file_name in files:
            if old_str in file_name:
                old_file_path = os.path.join(root, file_name)
                new_file_name = file_name.replace(old_str, new_str)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")

        # Replace content in files
        for file_name in files:
            file_path = os.path.join(root, file_name)
            replace_in_file(file_path, old_str, new_str)

# Specify the folder path and the strings to replace
folder_path = 'tests'
old_str = 'ragdoll'
new_str = 'quark'

# Perform the replacement
replace_in_filenames_and_contents(folder_path, old_str, new_str)
print("Replacement completed!")
