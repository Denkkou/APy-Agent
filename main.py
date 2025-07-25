import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.file_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.file_write import schema_write_file
from functions.file_contents import schema_get_file_content

from functions.file_info import get_files_info
from functions.file_contents import get_file_content 
from functions.file_write import write_file
from functions.run_python import run_python_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = ""
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    # Prompt
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("Error, no prompt argument given")
        return 1

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file,
            schema_get_file_content
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            )
        )

    # Flags
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Output
    if response.function_calls != None:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part)
            print(f"-> {function_call_result.parts[0].function_response.response}")
    
    print(f"\n{response.text}")


def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function {function_call_part.name}")
    
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }        

    function_name = function_call_part.name

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call_part.args)
    args.update({"working_directory": "./calculator"})

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

       

if __name__ == "__main__":
    main()