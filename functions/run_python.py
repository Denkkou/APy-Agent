import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if full_path.startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if os.path.exists(full_path) == False:
       return f'Error: File "{file_path}" not found.'

    if file_path.endswith(".py") == False:
        return f"Error: '{file_path}' is not a python file."
    
    try:
        new_args = ["python", full_path] + args
        result = subprocess.run(new_args, cwd=working_directory, timeout=30, capture_output=True)
    except:
        return f"Error: executing Python file {file_path}"
    
    stdout_string = f"STDOUT: {result.stdout}"
    stderr_string = f"STDERR: {result.stderr}"

    output_string = stdout_string + "\n" + stderr_string + "\n"

    if result.returncode != 0:
        output_string = output_string + f"Process exited with code {result.returncode}"

    if result.stdout == None:
        return "No output produced."

    return output_string