import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
    
    if os.path.isdir(full_path) == False:
        return f"Error: '{directory}' is not a directory"
    
    list_of_files = os.listdir(full_path)
    file_specifics = list(map(lambda x: file_details(full_path, x), list_of_files))  

    if directory == ".":
        dir = "current"
    else:
        dir = directory

    return f"Result for '{dir}' directory:\n" + "\n".join(file_specifics)
    

def file_details(directory, file):
    full_path = os.path.join(directory, file)

    size = os.path.getsize(full_path)
    is_dir = os.path.isdir(os.path.join(directory, file))
    
    return f"- {file}: file_size={size} bytes, is_dir={is_dir}"