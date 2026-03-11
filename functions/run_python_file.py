import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="command flags/args",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                
            ),
        },
    ),
)

#1
def run_python_file(working_directory, file_path, args=None):
    #2
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    #3
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    #4
    root, extension = os.path.splitext(file_path)
    if extension != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", file_path]
    if args != None:
        for arg in args:
            command.extend(arg)
    try:
        result = subprocess.run(command,cwd= working_dir_abs, capture_output=True, text=True, check=True, timeout=30000)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if result.stdout==None and result.stderr==None:
            return "No output produced"

        result_str = f'STDOUT: {result.stdout} \n STDERR: {result.stderr} \n' 

        return result_str
    except subprocess.CalledProcessError as e:
        return f"Error: executing Python file: {e}"



        