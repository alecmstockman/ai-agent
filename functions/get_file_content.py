from .config import MAX_CHARS
import google.genai as genai
from google.genai import types
import os

def get_file_content(working_directory, file_path):
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working = os.path.abspath(working_directory)

    if not abs_file.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(abs_file, "r", encoding="utf-8") as f:
        text = f.read(MAX_CHARS + 1)

        if len(text) > MAX_CHARS:
            truncation = f'[...File "{file_path}" truncated at 10000 characters]'
            # print(text[:MAX_CHARS])
            # print(truncation)
            return text[:MAX_CHARS], truncation
        else:
            return text

if __name__ == "__main__":
    get_file_content("calculator", "lorem.txt")


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns up to first {MAX_CHARS} characters of a specified file as a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory. ",
            ),
        },
        required=["file_path"],
    ),
)