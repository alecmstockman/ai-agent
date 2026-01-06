import os
import google.genai as genai
from google.genai import types

def write_file_content(working_directory, file_path, content):
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working = os.path.abspath(working_directory)
    dir_path = os.path.dirname(abs_file)
    
    if not abs_file.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        return f'Error: Cannot make {dir_path}: {e}'
    
    if os.path.isdir(abs_file):
        return f'Error: cannot over file as {file_path} is a directory, not a file'

    try:
        with open(abs_file, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error writing file '{file_path}': {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    


schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description=f"Takes content as a string and writes it to a file at the specified file path. If file already exists, it will be overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to write, relative to the working directory. ",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content as string that will be written to file at file_path."
            )
        },
        required=["file_path", "content"],
    ),
)