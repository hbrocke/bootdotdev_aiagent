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
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(working_dir_abs):
            return f'Error: "{working_dir_abs}" is not a directory'
    
        files = os.listdir(target_dir) 
        message = f"Result for { directory } directory: \n"
        for item in files:
            item_path = target_dir+"/"+item
            item_isdir = os.path.isdir(item_path)
            item_size = os.path.getsize(item_path)
            message += f"- {item}: file_size={item_size}, is_dir={item_isdir}\n" 
        return message
    except Exception as e:
        return f"Error: {e}"
