import os 
import google.genai as genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_directory = os.path.join(working_directory, directory)
    abs_working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(full_directory)

    if not abs_dir.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_directory):
        return f'Error: "{directory}" is not a directory'
    
    files = os.listdir(full_directory)
    files_list = []
    for file in files:
        file_name = os.path.join(full_directory, file)
        size = os.path.getsize(file_name)
        is_dir = os.path.isdir(file_name)
        files_list.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}" + "\n")

    output = "".join(files_list)
    return (output)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory. (Use '.' for the root/current directory.)",
            ),
        },
    ),
)

