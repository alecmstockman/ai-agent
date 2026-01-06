from functions.config import *
import os


def get_file_content(working_directory, file_path):

    if not abs_file.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(abs_file, "r", encoding="utf-8") as f:
        text = f.read(MAX_CHARS + 1)

        if len(text) > MAX_CHARS:
            truncation = f'[...File "{file_path}" truncated at 10000 characters]'
            print(len(text))
            print(truncation)
            
        else:
            print(text)


if __name__ == "__main__":
    get_file_content("calculator", "lorem.txt")
    get_file_content("calculator", "main.py")
    get_file_content("calculator", "pkg/calculator.py")
    get_file_content("calculator", "/bin/cat")
    get_file_content("calculator", "pkg/does_not_exist.py")
