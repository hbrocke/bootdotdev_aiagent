import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file ]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)
        cpo = subprocess.run(command, text=True, timeout=30,capture_output=True,cwd=working_directory)#,stdout=True, stderr=True)
        
        content = ""
        if cpo.returncode:
            content += f"Process exited with code {cpo.returncode}"
        if not cpo.stdout and not cpo.stderr:
            content += "No output produced"
        else:
            content += f"STDOUT: {cpo.stdout}"
            content += f"STDERR: {cpo.stderr}"

        return content 
        
    except Exception as e:
      return f"Error: executing Python file: {e}"
