import os 

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    
    #1:
    working_dir_abs = os.path.abspath(working_directory)
    # print(f'working_dir_abs = {working_dir_abs}')
    #print(f'directory = {directory}')
    #2:
    target_path = os.path.normpath(os.path.join(working_dir_abs, directory))
    #print(f'target_path = {target_path}')

    #3: 
    valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #4
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'
    
    dir_contents = os.listdir(os.path.abspath(target_path))
    ret_str =""
    if directory==".":
        ret_str = f'Result for current directory:\n'
    else:
        ret_str = f'Result for {directory} directory:\n'
    for item in dir_contents:
     #   print(f'item = {item}')   
        item_path = os.path.normpath(os.path.join(target_path, item))
        ret_str += f'- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n'
    return ret_str

        
