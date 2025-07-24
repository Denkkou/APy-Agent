from functions.file_info import get_files_info
from functions.file_contents import get_file_content 
from functions.file_write import write_file
from functions.run_python import run_python_file

def main():
    #print(get_files_info("calculator", "."))
    #print(get_files_info("calculator", "pkg"))
    #print(get_files_info("calculator", "/bin"))
    #print(get_files_info("calculator", "../"))

    #print(get_file_content("calculator", "main.py"))
    #print(get_file_content("calculator", "pkg/calculator.py"))
    #print(get_file_content("calculator", "/bin/cat"))
    #print(get_file_content("calculator", "/pkg/does_not_exists.py"))

    #print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    #print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    #print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))


if __name__ == "__main__":
    main()