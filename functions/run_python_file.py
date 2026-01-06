import os
import subprocess
import google.genai as genai
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working = os.path.abspath(working_directory)
    if args == None:
        add_args = []
    else:
        add_args = args

    if os.path.commonpath([abs_working, abs_file]) != abs_working:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmd = ["python", file_path] + add_args
        result = subprocess.run(cmd, cwd=abs_working, capture_output=True, timeout=30, text=True)
        if not result.stdout and not result.stderr:
            return "No output produced"
        if result.returncode != 0:
            return f"STDOUT: {result.stdout}, STDERR: {result.stderr}. Process exited with code {result.returncode}"
        return f'STDOUT: {result.stdout}, STDERR: {result.stderr}'
    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Executes a Python file located in the working directory and returns the program's stdout and stderr as a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory. ",
            ),
        },
        required=["file_path"],
    ),
)