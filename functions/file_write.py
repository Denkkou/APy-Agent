import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if full_path.startswith(os.path.abspath(working_directory)) == False:
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    if os.path.exists(full_path) == False:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    if os.path.exists(full_path) and os.path.isdir(full_path):
        return f"Error: '{file_path}' is a directory not a file"

    with open(full_path, "w") as f:
        f.write(content)
    
    return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Modifies or creates a file to contain given text, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text to be written to the file.",
            ),
        },
    ),
)