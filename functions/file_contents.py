import os
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if full_path.startswith(os.path.abspath(working_directory)) == False:
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    if exists_or_is_file(full_path) == False:
        return f"Error: File not found or is not a regular file: '{file_path}'" 
    
    file_content_string = ""

    with open(full_path, "r") as f:
        file_content_string = f.read()

        if len(file_content_string) > MAX_CHARS:
            return file_content_string[:MAX_CHARS] + f"\n[...File '{file_path}' truncated at {MAX_CHARS} characters]"
        else:
            return file_content_string

def exists_or_is_file(path):
    return (os.path.exists(path) or os.path.isfile(path))