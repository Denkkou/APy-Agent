import os

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if full_path.startswith(os.path.abspath(working_directory)) == False:
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    if os.path.exists(full_path) == False:
        os.makedirs(file_path)
    
    with open(full_path, "w") as f:
        f.write(content)
    
    return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
