import os

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content into a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="text content to be written"
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    #1
    working_dir_abs = os.path.abspath(working_directory)
    
    #2
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
     #3
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    #7
    try:
        #4
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        #5
        
        with open(target_path, "w") as f:
            f.write(content)
        
        #6
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    #7
    except:
        return f'Error: something went wrong!'
    