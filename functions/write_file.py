import os
from google.genai import types

schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Writes a content string to a file in a specified file path relative to the working directory, stating success or failure.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A String containing the letters that shall be written to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    print()
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file ]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        dirname, fname = os.path.split(target_file )
        os.makedirs(dirname, exist_ok=True)

        
        with open(target_file, "w") as f:
            ret_write = f.write(content)
        
        if ret_write:
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        return f'Error: Write to "{file_path}" not successfull'
        
    except Exception as e:
      return f"Error: {e}"
    